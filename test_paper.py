import argparse
import contextlib
import io
import json
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
        with contextlib.redirect_stdout(io.StringIO()):
            paper.initialize(self.root)

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
