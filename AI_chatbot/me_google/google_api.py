# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# When modifying these scopes, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def main():
    """
    Showing the basic usage of this People API.
    Prints the name of the first ten connections
    """
    creds = None

    # The file token.json stores the user's access and refresh token and is
    # created automtamatic automatically when the authorization
    # flow completes for the
    # first time
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # if there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
              "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    try:
        service = build("people", "v1", credentials=creds)

        # Calling the People API
        print("List 10 connection names")
        results = (
          service.people().connection()
          .list(
            resourceName="people/me",
            pageSize=10,
            personFields="names,emailAddresses",
          )
          .execute()
        )
        connections = results.get("connections", [])
        for person in connections:
            names = person.get("names", [])
            if names:
                name = names[0].get("displayName")
                print(name)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
        main()
