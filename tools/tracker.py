"""Create and update Cynthus issues with the properties the engineering standards require.

Usage as a library::

    tracker = Tracker()
    number = tracker.create_issue('cynthus-core', title='...', body='...', issue_type='Application Feature',
                                  milestone=3, priority='P1 - High', subtype='Application', applies_to='Cynthus Core')
    tracker.set_status('cynthus-core', number, 'In Progress')

Every created issue is assigned, typed, given a milestone and labels, added to the Cynthus Engineering Tracker project,
and given Priority, Subtype, Applies to, Status and Estimated Completion values.
"""

import json
import subprocess
import sys
from datetime import date, timedelta

ORG = 'TechClusiveSolutions'
PROJECT_NUMBER = 6
DEFAULT_ASSIGNEE = 'blindtechmage'


def gh(*args: str, stdin: str | None = None) -> str:
    """Run the GitHub CLI and return stdout, raising with the error text on failure."""

    result = subprocess.run(['gh', *args], input=stdin, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        raise RuntimeError(f'gh {" ".join(args)} failed: {result.stderr.strip()}')

    return result.stdout


class Tracker:
    """Thin wrapper over the GitHub CLI for the Cynthus Engineering Tracker project."""

    def __init__(self) -> None:
        self._project_id = json.loads(gh('project', 'view', str(PROJECT_NUMBER), '--owner', ORG, '--format', 'json'))['id']
        fields = json.loads(gh('project', 'field-list', str(PROJECT_NUMBER), '--owner', ORG, '--format', 'json',
                               '--limit', '50'))['fields']
        self._fields = {field['name']: field for field in fields}

    def _option_id(self, field: str, option: str) -> str:
        for candidate in self._fields[field]['options']:
            if candidate['name'] == option:
                return candidate['id']

        raise KeyError(f'{field} has no option {option!r}')

    def _milestone_number(self, repo: str, milestone: int | str) -> int:
        if isinstance(milestone, int):
            return milestone

        for item in json.loads(gh('api', f'repos/{ORG}/{repo}/milestones?state=all&per_page=50')):
            if item['title'] == milestone:
                return item['number']

        raise KeyError(f'{repo} has no milestone {milestone!r}')

    def add_to_project(self, repo: str, number: int) -> str:
        """Add the issue to the project and return the project item id."""

        out = gh('project', 'item-add', str(PROJECT_NUMBER), '--owner', ORG, '--url',
                 f'https://github.com/{ORG}/{repo}/issues/{number}', '--format', 'json')

        return json.loads(out)['id']

    def _set_select(self, item_id: str, field: str, option: str) -> None:
        gh('project', 'item-edit', '--id', item_id, '--project-id', self._project_id, '--field-id',
           self._fields[field]['id'], '--single-select-option-id', self._option_id(field, option))

    def _set_date(self, item_id: str, field: str, value: str) -> None:
        gh('project', 'item-edit', '--id', item_id, '--project-id', self._project_id, '--field-id',
           self._fields[field]['id'], '--date', value)

    def set_status(self, repo: str, number: int, status: str) -> None:
        item_id = self.add_to_project(repo, number)
        self._set_select(item_id, 'Status', status)

    def create_issue(self, repo: str, *, title: str, body: str, issue_type: str, milestone: int | str,
                     priority: str = 'P2 - Medium', subtype: str = 'Application', applies_to: str = 'Cynthus Core',
                     labels: tuple[str, ...] = ('Feature',), status: str = 'Backlog', days: int = 14,
                     parent: tuple[str, int] | None = None) -> int:
        """Create the issue with all required properties and return its number."""

        payload = {
            'title': title, 'body': body, 'type': issue_type, 'labels': list(labels),
            'milestone': self._milestone_number(repo, milestone), 'assignees': [DEFAULT_ASSIGNEE],
        }
        created = json.loads(gh('api', f'repos/{ORG}/{repo}/issues', '--input', '-', stdin=json.dumps(payload)))
        number = created['number']
        item_id = self.add_to_project(repo, number)
        self._set_select(item_id, 'Status', status)
        self._set_select(item_id, 'Priority', priority)
        self._set_select(item_id, 'Subtype', subtype)
        self._set_select(item_id, 'Applies to', applies_to)
        self._set_date(item_id, 'Estimated Completion', (date.today() + timedelta(days=days)).isoformat())

        if parent is not None:
            self.link_sub_issue(parent, (repo, number))

        return number

    def link_sub_issue(self, parent: tuple[str, int], child: tuple[str, int]) -> None:
        """Make ``child`` a native GitHub sub-issue of ``parent``."""

        child_id = json.loads(gh('api', f'repos/{ORG}/{child[0]}/issues/{child[1]}'))['id']
        gh('api', f'repos/{ORG}/{parent[0]}/issues/{parent[1]}/sub_issues', '-X', 'POST', '-F', f'sub_issue_id={child_id}')


def main() -> int:
    print(__doc__)

    return 0


if __name__ == '__main__':
    sys.exit(main())
