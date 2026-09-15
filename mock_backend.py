"""Offline integration-test fixture. NOT a real AI backend."""
import json
import sys

request = json.load(sys.stdin)
payload = request['payload']
schema = payload['schema']
if 'tasks' in schema:
    answer = {'questions': [], 'tasks': [{'id': 'T01', 'role': 'writer', 'goal': '标注资料缺口',
              'acceptance': '不捏造事实', 'depends_on': [], 'inputs': []}]}
elif 'verdict' in schema:
    answer = {'verdict': 'pass', 'feedback': '测试审核通过，不代表学术质量验证', 'needs_user': False}
elif 'summary' in schema:
    answer = {'summary': '测试运行完成，等待用户验收', 'questions': []}
else:
    answer = {'content': '# 测试产物\n资料尚未提供，不形成研究结论。', 'needs_user': False, 'questions': []}
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(answer, ensure_ascii=False))
sys.stdout.flush()
