"""Move portal tasks to Done from commit messages.

Reads the pushed commits (COMMITS_JSON = toJSON(github.event.commits)), finds
"Closes Task N" (also "Close/Closed/Fixes/Resolves Task N", "Closes Tasks 1, 3 and 4",
"Closes Task #2"), and updates the task board file (PORTAL_FILE, the portal's data.js):
status -> "done", docLink -> the commit URL (if the task has no link yet).

Writes "changed=true|false" and "tasks=..." to $GITHUB_OUTPUT and a short report to
$GITHUB_STEP_SUMMARY. Never fails the push: unknown task numbers are reported as warnings.
"""
import datetime as dt
import json
import os
import re
import sys

CLOSE_RE = re.compile(
    r'\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+tasks?\s*#?\s*'
    r'(\d+(?:\s*(?:,|&|and)\s*(?:task\s*)?#?\s*\d+)*)',
    re.IGNORECASE)


def today_cairo():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo('Africa/Cairo')).date().isoformat()
    except Exception:  # tz database missing: UTC is close enough for a date stamp
        return dt.datetime.now(dt.timezone.utc).date().isoformat()


def closed_tasks(commits):
    """Return [(task_number_str, commit)] in push order, first mention wins."""
    seen, out = set(), []
    for c in commits:
        for m in CLOSE_RE.finditer(c.get('message', '')):
            for n in re.findall(r'\d+', m.group(1)):
                n = str(int(n))
                if n not in seen:
                    seen.add(n)
                    out.append((n, c))
    return out


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # emoji in the report on any console
    commits = json.loads(os.environ.get('COMMITS_JSON') or '[]')
    path = os.environ.get('PORTAL_FILE', 'portal/data.js')
    report, changed = [], []

    todo = closed_tasks(commits)
    if not todo:
        print('No "Closes Task N" in the pushed commits; nothing to do.')
        emit(False, [], ['No "Closes Task N" found in this push.'])
        return

    src = open(path, encoding='utf-8').read()
    head, body = src[:src.index('{')], src[src.index('{'):src.rindex('}') + 1]
    data = json.loads(body)
    tasks = {str(t.get('code')): t for t in data.get('tasks', [])}
    groups = data.get('groups', [])

    def phase_locked(task):
        g = next((x for x in groups if x['id'] == task['group']), None)
        if not g or not g.get('gated'):
            return None
        same = [x for x in groups if x.get('category') == g.get('category')]
        i = same.index(g)
        if i == 0:
            return None
        prev = same[i - 1]
        open_ = [t for t in data['tasks'] if t['group'] == prev['id'] and t.get('status') != 'done']
        return prev.get('short', prev['id']).split('·')[0].strip() if open_ else None

    for n, commit in todo:
        t = tasks.get(n)
        who = (commit.get('author') or {}).get('name') or (commit.get('author') or {}).get('username') or 'someone'
        if not t:
            print(f'::warning::Commit {commit.get("id", "")[:7]} closes Task {n}, but the board has no Task {n}.')
            report.append(f'- ⚠️ Task {n}: not on the board (commit `{commit.get("id", "")[:7]}`)')
            continue
        if t.get('status') == 'done' and t.get('docLink'):
            report.append(f'- Task {n} "{t["title"]}" was already Done')
            continue
        lock = phase_locked(t)
        if lock:
            print(f'::warning::Task {n} closed while its phase is still locked ({lock} is not 100% done).')
            report.append(f'- ⚠️ Task {n} closed although {lock} is not 100% done yet')
        t['status'] = 'done'
        if not t.get('docLink') and commit.get('url'):
            t['docLink'] = commit['url']
        changed.append(n)
        report.append(f'- ✅ Task {n} "{t["title"]}" → Done (by {who}, commit `{commit.get("id", "")[:7]}`)')

    if changed:
        data.setdefault('project', {})['lastUpdated'] = today_cairo()
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(head + json.dumps(data, indent=2, ensure_ascii=False) + ';\n')
    print('\n'.join(report))
    emit(bool(changed), changed, report)


def emit(changed, tasks, report):
    out = os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out, 'a', encoding='utf-8') as f:
            f.write(f'changed={"true" if changed else "false"}\n')
            f.write(f'tasks={", ".join(tasks)}\n')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write('### Task board update\n' + '\n'.join(report) + '\n')


if __name__ == '__main__':
    sys.exit(main())
