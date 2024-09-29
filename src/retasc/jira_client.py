import logging

from atlassian import Jira

logger = logging.getLogger(__name__)


class JiraClient:
    """
    Jira Client Wrapper
    """

    def __init__(self, api_url: str, token: str | None = None):
        self.api_url = api_url
        self.jira = Jira(
            url=api_url,
            token=token,
        )

    def api_url_issue(self, issue_key: str | None = None) -> str:
        return f"{self.api_url.rstrip('/')}/rest/api/2/issue/{issue_key or ''}"

    def api_url_create_issue(self) -> str:
        # The "?updateHistory=false" is the default url for jira.create_issue to connect
        # with JIRA and the retasc will not use the way of updateHistory=ture at all
        return f"{self.api_url.rstrip('/')}/rest/api/2/issue?updateHistory=false"

    def api_url_edit_issue(self, issue_key: str, notify_users: bool = True) -> str:
        return f"{self.api_url.rstrip('/')}/rest/api/2/issue/{issue_key}?notifyUsers={notify_users}"

    def api_url_search_issue(self) -> str:
        return f"{self.api_url.rstrip('/')}/rest/api/2/search?startAt=0&fields=%2Aall&jql=project+%3D+TEST"

    def edit_issue(self, issue_key: str, fields: dict, notify_users: bool = True) -> None:
        """
        Updates a Jira issue with the provided fields.

        :param issue_key: The key of the Jira issue to update.
        :param fields: A dictionary of fields to update in the issue.
                    example:
                        fields = {
                            'project': {'key': 'RHELWF'},
                            'summary': '[ReTaSC] Default summary',
                            'description': 'Default description - please update this description.',
                            'issuetype': {'name': 'Story'},
                            'priority': {'name':'Normal'}
                        }
        :return:
        :if not found: requests.exceptions.HTTPError: Issue Does Not Exist
        """

        logger.info("Updating Jira issue %r with fields: %r", issue_key, fields)
        self.jira.edit_issue(issue_key, fields, notify_users=notify_users)

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str,
        fields: dict = {},
    ) -> dict:
        """
        Create a new Jira issue
        """

        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }

        issue_dict.update(fields)

        logger.info("Creating new Jira issue with fields: %r", issue_dict)

        issue = self.jira.create_issue(issue_dict)
        return issue

    def search_issue(self, JQL: str) -> list:
        """
        Search Issues by JQL

        :param JQL: string: like "project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey"
        """

        issue_list = self.jira.jql(JQL)
        return issue_list

    def get_issue(self, issue_key: str) -> dict:
        """
        Get a Jira issue.
        """

        issue = self.jira.issue(issue_key)
        return issue
