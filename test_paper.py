import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import sys
import unittest
from unittest.mock import patch
import paper


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)/'论文 workspace'
        # 本机用户主目录本身是 Git 仓库；阻止 git 向上发现，避免临时工作区被误判为嵌套仓库。
        os.environ['GIT_CEILING_DIRECTORIES'] = self.tmp.name
        with contextlib.redirect_stdout(io.StringIO()):
            paper.initialize(self.root)
        paper.git(self.root, 'config', 'user.email', 'test@example.com')
        paper.git(self.root, 'config', 'user.name', 'Test')

    def tearDown(self):
        self.tmp.cleanup()

    def test_init_git_and_all_indexes(self):
        self.assertTrue((self.root/'.git').is_dir())
        for folder, _ in paper.walk(self.root):
            self.assertTrue((folder/'index.md').is_file(), folder)
        self.assertEqual(paper.git(self.root, 'diff', '--cached', '--name-only').stdout, '')

    def test_repeat_preserves_content(self):
        p = self.root/'AGENTS.md'
        p.write_text('用户规则', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            paper.initialize(self.root)
        self.assertEqual(p.read_text(encoding='utf-8'), '用户规则')

    def test_indexes_stable_and_delete(self):
        self.assertEqual(paper.index(self.root), 0)
        initial = (self.root/'index.md').read_bytes()
        self.assertEqual(paper.index(self.root), 0)
        self.assertEqual(initial, (self.root/'index.md').read_bytes())
        p = self.root/'notes/user.md'
        p.write_text('用户想法', encoding='utf-8')
        self.assertEqual(paper.index(self.root), 1)
        p.write_text('新的想法', encoding='utf-8')
        self.assertEqual(paper.index(self.root), 1)
        p.unlink()
        self.assertEqual(paper.index(self.root), 1)
        idx = (self.root/'notes/index.md').read_text(encoding='utf-8')
        for word in ['新增', '修改', '删除']:
            self.assertIn(word, idx)

    def test_preserve_index_prose(self):
        p = self.root/'notes/index.md'
        p.write_text('我的目录说明\n' + p.read_text(encoding='utf-8') + '\n我的备注\n', encoding='utf-8')
        paper.index(self.root)
        self.assertTrue(p.read_text(encoding='utf-8').startswith('我的目录说明'))
        self.assertTrue(p.read_text(encoding='utf-8').endswith('我的备注\n'))

    def test_symlink_escape(self):
        try:
            (self.root/'notes/link').symlink_to(Path(self.tmp.name), target_is_directory=True)
        except OSError:
            self.skipTest('symlink privileges unavailable')
        with self.assertRaises(ValueError):
            paper.safe(self.root, 'notes/link/secret.txt')
        with self.assertRaises(ValueError):
            paper.safe(self.root, '../secret')

    def test_nested_repository_rejected(self):
        with self.assertRaises(ValueError):
            paper.initialize(self.root/'nested')

    def test_lock(self):
        with paper.lock(self.root):
            with self.assertRaises(ValueError):
                with paper.lock(self.root):
                    pass

    def test_decision_conflict_and_supersession(self):
        a = {'id': 'DEC-a', 'subject': 'method', 'status': 'confirmed'}
        b = {'id': 'DEC-b', 'subject': 'method', 'status': 'confirmed'}
        paper.atomic(self.root/'decisions/DEC-a.json', paper.dump(a))
        paper.atomic(self.root/'decisions/DEC-b.json', paper.dump(b))
        with self.assertRaises(ValueError):
            paper.confirmed(self.root)
        b['supersedes'] = 'DEC-a'
        paper.atomic(self.root/'decisions/DEC-b.json', paper.dump(b))
        self.assertEqual(paper.confirmed(self.root), [b])

    def test_dependency_and_input_validation(self):
        task = {'id': 'T01', 'role': 'writer', 'goal': '写作', 'acceptance': '有依据', 'depends_on': ['T01']}
        with self.assertRaises(ValueError):
            paper.validate_plan({'tasks': [task]}, 8, [])
        task['depends_on'] = []
        task['inputs'] = ['materials/private/secret.txt']
        with self.assertRaises(ValueError):
            paper.validate_plan({'tasks': [task]}, 8, [])

    def args(self):
        return argparse.Namespace(brief='.paper-ai/templates/brief.md', input=[], dry_run=False, allow_model_calls=True)

    def fake_plan(self):
        return {'questions': [], 'tasks': [{'id': 'T01', 'role': 'writer', 'goal': '整理待确认问题',
                'acceptance': '不编造', 'depends_on': [], 'inputs': []}]}

    def test_pm_revise_review_loop(self):
        answers = [self.fake_plan(), {'content': '初稿'}, {'verdict': 'revise', 'feedback': '标明缺口'},
                   {'content': '修订稿：数据待提供'}, {'verdict': 'pass'}, {'summary': '待用户验收'}]
        with patch('paper.call_agent', side_effect=answers) as mocked, contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, self.args())
        self.assertEqual([c.args[2] for c in mocked.call_args_list], ['pm', 'writer', 'reviewer', 'writer', 'reviewer', 'pm'])
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'awaiting_user_acceptance')
        self.assertEqual(state['tasks'][0]['status'], 'review_passed')
        self.assertEqual(list((self.root/'writing/chapters').glob('*.md')), [self.root/'writing/chapters/index.md'])

    def test_pm_questions_pause(self):
        with patch('paper.call_agent', return_value={'questions': ['学校允许什么研究方法？']}), contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, self.args())
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'awaiting_user')

    def test_disabled_backend_fails_closed(self):
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            paper.run(self.root, self.args())
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'blocked')

    def test_private_and_budget(self):
        p = self.root/'materials/private/x.txt'
        p.write_text('private', encoding='utf-8')
        with self.assertRaises(ValueError):
            paper.context_files(self.root, ['materials/private/x.txt'], 1000)
        with self.assertRaises(ValueError):
            paper.context_files(self.root, ['.paper-ai/templates/brief.md'], 10)

    def test_deleted_directory_recorded_at_root(self):
        child = self.root/'notes/temporary'
        child.mkdir()
        (child/'note.md').write_text('notes', encoding='utf-8')
        paper.index(self.root)
        (child/'note.md').unlink()
        (child/'index.md').unlink()
        child.rmdir()
        paper.index(self.root)
        self.assertIn('notes/temporary/note.md', (self.root/'index.md').read_text(encoding='utf-8'))

    def test_decision_cycle(self):
        for a, b in [('a', 'b'), ('b', 'a')]:
            paper.atomic(self.root/f'decisions/DEC-{a}.json', paper.dump({'id': a, 'subject': 'method', 'status': 'confirmed', 'supersedes': b}))
        with self.assertRaises(ValueError):
            paper.confirmed(self.root)

    def test_real_subprocess_offline_fixture(self):
        config = paper.load(self.root/'workspace.json')
        config['default_backend'] = 'test-only'
        paper.atomic(self.root/'workspace.json', paper.dump(config))
        paper.atomic(self.root/'.paper-ai/adapters/backends.json', paper.dump({'test-only': {
            'enabled': True, 'command': [sys.executable, str(Path(__file__).parent/'mock_backend.py')], 'response': 'stdout'}}))
        with contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, self.args())
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'awaiting_user_acceptance')
        self.assertTrue((self.root/state['tasks'][0]['artifact']).exists())

    def test_dry_run_no_model(self):
        args = self.args()
        args.dry_run = True
        with patch('paper.call_agent') as mocked, contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, args)
        mocked.assert_not_called()

    def test_decision_quote_exact(self):
        quote = '保留原有案例研究，不改成问卷。'
        paper.atomic(self.root/'notes/quote.txt', quote)
        args = argparse.Namespace(evidence='notes/quote.txt', source_ref='用户消息#1',
                                  subject='method', text='保留案例研究', supersedes=None,
                                  confirm=True, affects=['writing/outline'], reason='用户确认')
        with contextlib.redirect_stdout(io.StringIO()):
            paper.decision(self.root, args)
        item = paper.confirmed(self.root)[0]
        self.assertEqual(item['quote'], quote)
        self.assertEqual(item['status'], 'confirmed')

    def decision_args(self, **kw):
        paper.atomic(self.root/'notes/quote.txt', kw.get('quote', '用户原话'))
        return argparse.Namespace(evidence='notes/quote.txt', source_ref='用户消息#1',
                                  subject=kw.get('subject', 'formatting'), text=kw.get('text', '登记格式规范'),
                                  supersedes=None, affects=[], confirm=kw.get('confirm', True),
                                  reason=kw.get('reason', '用户确认'), guideline=kw.get('guideline'))

    def test_decision_guideline_confirmed_registers_and_replaces(self):
        paper.atomic(self.root/'materials/guidelines/school.md', '学校规范\n')
        args = self.decision_args(guideline='file=materials/guidelines/school.md,title=校规范,version=2026,locator=第3章')
        with contextlib.redirect_stdout(io.StringIO()):
            paper.decision(self.root, args)
        expected = [{'file': 'materials/guidelines/school.md', 'title': '校规范',
                     'version_or_date': '2026', 'locator': '第3章'}]
        self.assertEqual(paper.load(self.root/'workspace.json')['formatting_guidelines'], expected)
        self.assertEqual(len(list((self.root/'decisions').glob('DEC-*.json'))), 1)
        args2 = self.decision_args(guideline='file=materials/guidelines/school.md,title=校规范,version=2027')
        with contextlib.redirect_stdout(io.StringIO()):
            paper.decision(self.root, args2)
        config = paper.load(self.root/'workspace.json')
        self.assertEqual(len(config['formatting_guidelines']), 1)
        self.assertEqual(config['formatting_guidelines'][0]['version_or_date'], '2027')

    def test_decision_guideline_proposed_not_written(self):
        paper.atomic(self.root/'materials/guidelines/school.md', '学校规范\n')
        args = self.decision_args(confirm=False, guideline='file=materials/guidelines/school.md,title=校规范')
        with contextlib.redirect_stdout(io.StringIO()):
            paper.decision(self.root, args)
        self.assertEqual(paper.load(self.root/'workspace.json')['formatting_guidelines'], [])
        item = paper.load(next((self.root/'decisions').glob('DEC-*.json')))
        self.assertEqual(item['status'], 'proposed')

    def test_decision_guideline_path_and_existence_validated(self):
        with self.assertRaises(ValueError):
            paper.decision(self.root, self.decision_args(guideline='file=../outside.md,title=x'))
        with self.assertRaises(ValueError):
            paper.decision(self.root, self.decision_args(guideline='file=materials/guidelines/nope.md,title=x'))
        with self.assertRaises(ValueError):
            paper.decision(self.root, self.decision_args(guideline='file=materials/guidelines,title=x'))
        with self.assertRaises(ValueError):
            paper.decision(self.root, self.decision_args(guideline='title=x'))
        with self.assertRaises(ValueError):
            paper.decision(self.root, self.decision_args(guideline='file=materials/guidelines/nope.md,title=x,foo=1'))

    def test_input_changes_during_worker_stop(self):
        def fake(root, config, role, payload, call_dir):
            if role == 'pm':
                return self.fake_plan()
            paper.atomic(root/'.paper-ai/templates/brief.md', '内容被人工更改')
            return {'content': '旧依据生成内容'}
        with patch('paper.call_agent', side_effect=fake), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            paper.run(self.root, self.args())
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'blocked')

    def test_malformed_index_fails_closed(self):
        p = self.root/'notes/index.md'
        paper.atomic(p, paper.END + '\n' + paper.BEGIN)
        with self.assertRaises(ValueError):
            paper.index(self.root)

    def test_init_issues_templates_and_guidelines_field(self):
        idx = self.root/'notes/issues/index.md'
        self.assertTrue(idx.is_file())
        for word in ['编号', '问题摘要', '维度', '状态', '提出日期', '解决日期']:
            self.assertIn(word, idx.read_text(encoding='utf-8'))
        tpl = self.root/'notes/issues/ISS-001-template.md'
        self.assertTrue(tpl.is_file())
        for word in ['id', 'status', 'dimension', 'created', 'resolved', '提问时的上下文', '待澄清内容']:
            self.assertIn(word, tpl.read_text(encoding='utf-8'))
        for rel in ['writing/spec/index.md', 'writing/plan/index.md', 'materials/guidelines/index.md']:
            self.assertTrue((self.root/rel).is_file(), rel)
        self.assertEqual(paper.load(self.root/'workspace.json')['formatting_guidelines'], [])

    def reset_args(self, topic, **kw):
        return argparse.Namespace(topic=topic, confirm=kw.get('confirm', False),
                                  allow_unicode_branch=kw.get('allow_unicode', False),
                                  branch_only=kw.get('branch_only', False))

    def seed_topic_artifacts(self):
        paper.atomic(self.root/'decisions/DEC-seed.json', paper.dump({'id': 'DEC-seed', 'subject': 'topic', 'status': 'confirmed'}))
        paper.atomic(self.root/'tasks/RUN-seed.json', paper.dump({'id': 'RUN-seed', 'status': 'done'}))
        paper.atomic(self.root/'notes/issues/ISS-002-延后.md', '# 延后问题\n')
        paper.atomic(self.root/'writing/outline/outline.md', '# 旧大纲\n')
        paper.atomic(self.root/'writing/chapters/ch1.md', '# 旧章节\n')
        paper.atomic(self.root/'writing/drafts/draft.md', '# 旧草稿\n')
        paper.atomic(self.root/'references/ref.bib', '@book{x}\n')
        paper.atomic(self.root/'output/v1.0-release/result.md', '# 旧产物\n')
        paper.atomic(self.root/'materials/guidelines/school.md', '学校规范原件\n')
        paper.atomic(self.root/'AGENTS.md', '用户合并的规则\n')
        config = paper.load(self.root/'workspace.json')
        config.update({'topic': '旧主题', 'school_requirements': '旧要求', 'ai_disclosure_policy': '旧政策',
                       'formatting_guidelines': [{'file': 'materials/guidelines/school.md', 'title': '校规范',
                                                  'version_or_date': '2026', 'locator': '第3章'}]})
        paper.atomic(self.root/'workspace.json', paper.dump(config))

    def test_reset_topic_slugify(self):
        self.assertEqual(paper.slugify('Hello World_2.0?'), 'hello-world-2.0')
        self.assertEqual(paper.slugify('a b~c^d:e'), 'a-bcde')
        self.assertEqual(len(paper.slugify('x' * 100)), 48)
        with self.assertRaises(ValueError):
            paper.slugify('我的主题')
        self.assertEqual(paper.slugify('我的主题', allow_unicode=True), '我的主题')
        with self.assertRaises(ValueError):
            paper.slugify('???')

    def test_reset_topic_plan_backs_up_without_branch(self):
        self.assertNotEqual(paper.git(self.root, 'rev-parse', '--verify', 'HEAD', check=False).returncode, 0)
        self.seed_topic_artifacts()
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('New Topic 2.0'))
        branches = paper.git(self.root, 'branch', '--list', 'feature-*').stdout
        self.assertNotIn('feature-new-topic-2.0', branches)
        self.assertEqual(paper.git(self.root, 'rev-parse', '--verify', 'HEAD', check=False).returncode, 0)
        self.assertTrue((self.root/'decisions/DEC-seed.json').is_file())

    def test_reset_topic_confirm_clears_and_preserves(self):
        self.seed_topic_artifacts()
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('Topic B', confirm=True))
        self.assertEqual(paper.git(self.root, 'branch', '--show-current').stdout.strip(), 'feature-topic-b')
        config = paper.load(self.root/'workspace.json')
        self.assertEqual(config['topic'], '')
        self.assertEqual(config['school_requirements'], '')
        self.assertEqual(config['ai_disclosure_policy'], '')
        self.assertEqual(config['formatting_guidelines'], [])
        self.assertFalse((self.root/'decisions/DEC-seed.json').exists())
        self.assertFalse((self.root/'tasks/RUN-seed.json').exists())
        self.assertFalse((self.root/'notes/issues/ISS-002-延后.md').exists())
        self.assertTrue((self.root/'notes/issues/ISS-001-template.md').is_file())
        self.assertFalse((self.root/'writing/outline/outline.md').exists())
        self.assertTrue((self.root/'writing/outline/index.md').is_file())
        self.assertFalse((self.root/'writing/chapters/ch1.md').exists())
        self.assertTrue((self.root/'writing/chapters/index.md').is_file())
        self.assertFalse((self.root/'writing/drafts/draft.md').exists())
        self.assertTrue((self.root/'writing/drafts/index.md').is_file())
        self.assertFalse((self.root/'references/ref.bib').exists())
        self.assertFalse((self.root/'output/v1.0-release').exists())
        self.assertTrue((self.root/'output/index.md').is_file())
        self.assertTrue((self.root/'writing/spec/index.md').is_file())
        self.assertEqual((self.root/'materials/guidelines/school.md').read_text(encoding='utf-8'), '学校规范原件\n')
        self.assertEqual((self.root/'AGENTS.md').read_text(encoding='utf-8'), '用户合并的规则\n')
        # 清空结果留在新分支工作区未提交，便于用户审阅差异；备份提交已在原分支之前完成。
        self.assertIn('D decisions/DEC-seed.json', paper.git(self.root, 'status', '--porcelain').stdout)

    def test_reset_topic_branch_exists_rejected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('Dup', confirm=True))
        with self.assertRaises(ValueError):
            with contextlib.redirect_stdout(io.StringIO()):
                paper.reset_topic(self.root, self.reset_args('Dup'))

    def test_reset_topic_branch_only_keeps_content(self):
        self.seed_topic_artifacts()
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('Iter', confirm=True, branch_only=True))
        self.assertEqual(paper.git(self.root, 'branch', '--show-current').stdout.strip(), 'feature-iter')
        self.assertTrue((self.root/'decisions/DEC-seed.json').is_file())
        self.assertEqual(paper.load(self.root/'workspace.json')['topic'], '旧主题')

    def test_reset_topic_via_main_cli(self):
        argv = ['paper.py', 'reset-topic', '--root', str(self.root), '--topic', 'Cli', '--confirm']
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(paper.main(), 0)
        self.assertEqual(paper.git(self.root, 'branch', '--show-current').stdout.strip(), 'feature-cli')

    def test_reset_topic_confirm_with_unborn_head(self):
        self.assertNotEqual(paper.git(self.root, 'rev-parse', '--verify', 'HEAD', check=False).returncode, 0)
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('Fresh Start', confirm=True))
        self.assertEqual(paper.git(self.root, 'branch', '--show-current').stdout.strip(), 'feature-fresh-start')
        self.assertEqual(paper.git(self.root, 'rev-parse', '--verify', 'HEAD', check=False).returncode, 0)
        self.assertEqual(paper.load(self.root/'workspace.json')['topic'], '')

    def test_reset_topic_preflight_fails_before_any_change(self):
        self.seed_topic_artifacts()
        head_before = paper.ensure_backup_commit(self.root, 'seed baseline')
        (self.root/'workspace.json').write_text('{损坏的json', encoding='utf-8')
        with self.assertRaises(ValueError) as ctx:
            paper.reset_topic(self.root, self.reset_args('Clean', confirm=True))
        msg = str(ctx.exception)
        self.assertIn('backup_commit', msg)
        self.assertIn('git checkout', msg)
        self.assertIn(head_before[:12], msg)
        self.assertTrue((self.root/'decisions/DEC-seed.json').is_file())
        self.assertEqual(paper.git(self.root, 'branch', '--list', 'feature-clean').stdout, '')
        self.assertEqual(paper.git(self.root, 'rev-parse', 'HEAD').stdout.strip(), head_before)
        self.assertEqual((self.root/'workspace.json').read_text(encoding='utf-8'), '{损坏的json')

    def test_reset_topic_backup_commit_falls_back_to_head(self):
        with contextlib.redirect_stdout(io.StringIO()):
            paper.reset_topic(self.root, self.reset_args('Quiet'))
        head = paper.git(self.root, 'rev-parse', 'HEAD').stdout.strip()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            paper.reset_topic(self.root, self.reset_args('Quiet Two'))
        plan = json.loads(buf.getvalue())
        self.assertEqual(plan['backup_commit'], head)

    def test_reset_topic_clear_unlinks_symlink_without_safe(self):
        self.seed_topic_artifacts()
        link = self.root/'writing/outline/old-link'
        try:
            link.symlink_to(self.root/'references', target_is_directory=True)
        except OSError:
            self.skipTest('symlink privileges unavailable')
        removed = paper.clear_topic_artifacts(self.root)
        self.assertIn('writing/outline/old-link', removed)
        self.assertFalse(link.exists() or link.is_symlink())

    def test_run_guidelines_injected_and_missing_file_warns(self):
        paper.atomic(self.root/'materials/guidelines/school.md', '学校规范条款\n')
        config = paper.load(self.root/'workspace.json')
        config['formatting_guidelines'] = [
            {'file': 'materials/guidelines/school.md', 'title': '校规范', 'version_or_date': '2026', 'locator': '第3章'},
            {'file': 'materials/guidelines/missing.md', 'title': '缺失规范'}]
        paper.atomic(self.root/'workspace.json', paper.dump(config))
        answers = [self.fake_plan(), {'content': '初稿'}, {'verdict': 'pass'}, {'summary': '待验收'}]
        with patch('paper.call_agent', side_effect=answers) as mocked, contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, self.args())
        pm_payload = mocked.call_args_list[0].args[3]
        self.assertEqual(len(pm_payload['guidelines']), 1)
        pointer = pm_payload['guidelines'][0]
        self.assertEqual(pointer['sha256'], paper.fingerprint(self.root/'materials/guidelines/school.md')[:12])
        self.assertEqual(pointer['locator'], '第3章')
        writer_payload = mocked.call_args_list[1].args[3]
        self.assertEqual(writer_payload['guidelines'], pm_payload['guidelines'])
        reviewer_payload = mocked.call_args_list[2].args[3]
        self.assertEqual(reviewer_payload['guidelines'], pm_payload['guidelines'])
        self.assertIn('规范符合性（按登记的 formatting_guidelines 检查排版要求）', reviewer_payload['review_focus'])
        state = paper.load(next((self.root/'tasks').glob('RUN-*.json')))
        self.assertEqual(state['status'], 'awaiting_user_acceptance')
        self.assertEqual(len(state['warnings']), 1)
        self.assertIn('missing.md', state['warnings'][0])

    def test_review_focus_without_guidelines(self):
        answers = [self.fake_plan(), {'content': '初稿'}, {'verdict': 'pass'}, {'summary': '总结'}]
        with patch('paper.call_agent', side_effect=answers) as mocked, contextlib.redirect_stdout(io.StringIO()):
            paper.run(self.root, self.args())
        reviewer_payload = mocked.call_args_list[2].args[3]
        self.assertEqual(reviewer_payload['review_focus'], paper.REVIEW_FOCUS_BASE)
        self.assertEqual(reviewer_payload['guidelines'], [])

    def test_resolve_guidelines_fail_closed_and_oversized(self):
        with self.assertRaises(ValueError):
            paper.resolve_guidelines(self.root, {'formatting_guidelines': '不是数组'})
        pointers, warnings = paper.resolve_guidelines(self.root, {'formatting_guidelines': [{'title': '缺file'}]})
        self.assertEqual(pointers, [])
        self.assertEqual(len(warnings), 1)
        with self.assertRaises(ValueError):
            paper.resolve_guidelines(self.root, {'formatting_guidelines': [{'file': '../escape.md', 'title': 'x'}]})
        big = self.root/'materials/guidelines/big.md'
        with big.open('wb') as f:
            f.seek(paper.MAX_GUIDELINE_BYTES)
            f.write(b'x')
        pointers, warnings = paper.resolve_guidelines(self.root, {'formatting_guidelines': [
            {'file': 'materials/guidelines/big.md', 'title': '超大规范'}]})
        self.assertTrue(pointers[0]['oversized'])
        self.assertIsNone(pointers[0]['sha256'])
        self.assertTrue(any('20MB' in w for w in warnings))

    def test_output_version_name_warning(self):
        (self.root/'output/v1.0-beta').mkdir()
        (self.root/'output/v1.0-release').mkdir()
        (self.root/'output/release-notes').mkdir()
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            paper.index(self.root)
        err = buf.getvalue()
        self.assertIn('v1.0-beta', err)
        self.assertIn('release-notes', err)
        self.assertNotIn('v1.0-release', err)


if __name__ == '__main__':
    unittest.main(verbosity=2)
