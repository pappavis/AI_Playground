# AI helpdesk assistant
THis prompt initaites a Powr Automate workflow in Microsoft Copilot.

**Prompt: Create Power Automate Flow - FEMSupport_EscalationHandler (UUID: 7C8D9E0F)**

# The prompt


**# FLOW_NAME:** FEMSupport_EscalationHandler

**# FLOW_METADATA:**
- Owner: ABCSupport AI Team
- Category: Support Escalation
- Tags: AI, ABC, escalation, HALO, logging

**# FLOW_DESCRIPTION:**
This Power Automate flow handles the escalation of unresolved FEM user issues from the AI Copilot. It sends an email notification, creates a HALO ticket, and logs the conversation context to a SharePoint list. The flow is designed to ensure all steps complete even if individual actions encounter issues.

**# TRIGGER:**
- **Type:** HTTP Request (When an HTTP request is received)
- **Method:** POST
- **Request Body JSON Schema:**
    ```json
    {
        "type": "object",
        "properties": {
            "userName": {
                "type": "string",
                "description": "Name of the user experiencing the issue."
            },
            "dateTime": {
                "type": "string",
                "format": "date-time",
                "description": "Date and time of the conversation."
            },
            "problemSummary": {
                "type": "string",
                "description": "A concise summary of the user's problem."
            },
            "aiResponse": {
                "type": "string",
                "description": "The last response provided by the AI before escalation."
            },
            "fullConversationContext": {
                "type": "string",
                "description": "The complete transcript or context of the conversation, preferably in JSON string format."
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Relevant tags for the issue (e.g., 'error_409', 'booking_issue')."
            }
        },
        "required": [
            "userName",
            "dateTime",
            "problemSummary",
            "aiResponse",
            "fullConversationContext",
            "tags"
        ]
    }
    ```

**# ACTIONS:**

**1. Initialize Variables (BEFORE SCOPES):**
    - **`varUserName`**: String. Value: `triggerBody()['userName']`
    - **`varDateTime`**: String. Value: `triggerBody()['dateTime']`
    - **`varProblemSummary`**: String. Value: `triggerBody()['problemSummary']`
    - **`varAIResponse`**: String. Value: `triggerBody()['aiResponse']`
    - **`varFullConversationContext`**: String. Value: `string(triggerBody()['fullConversationContext'])` (Ensure it's converted to string if original is JSON object)
    - **`varTags`**: String. Value: `join(triggerBody()['tags'], ', ')` (Convert array of tags to comma-separated string)
    - **`varHaloTicketID`**: String. Initial Value: `''`

**2. Scope: Send Email Notification (Scope_EmailNotification)**
    - **Action:** `Send an email (V2)` (Outlook connector)
    - **To:** `m.czabinski@fugro.com`
    - **Subject:** "FEMSupport Escalation – Unresolved Issue"
    - **Body (HTML):**
        ```html
        <p>Dear FEM Support Team,</p>
        <p>An issue has been escalated by the FEMSupport AI chatbot. Details are as follows:</p>
        <ul>
            <li><strong>User Name:</strong> @{variables('varUserName')}</li>
            <li><strong>Date and Time:</strong> @{variables('varDateTime')}</li>
            <li><strong>Summary of Problem:</strong> @{variables('varProblemSummary')}</li>
            <li><strong>AI Response:</strong> @{variables('varAIResponse')}</li>
            <li><strong>Resolution Status:</strong> UNRESOLVED</li>
            <li><strong>Tags:</strong> @{variables('varTags')}</li>
        </ul>
        <p><strong>Full Conversation Context:</strong></p>
        <pre>@{variables('varFullConversationContext')}</pre>
        <p>Please investigate this matter further.</p>
        <p>Best regards,<br>FEMSupport AI</p>
        ```
    - **Configure Run After:** No preceding actions for the first scope.

**3. Scope: Create HALO Ticket (Scope_CreateHALOTicket)**
    - **Action:** `HTTP` (or relevant HALO integration)
    - **Method:** `POST`
    - **URI:** `[Your HALO API Endpoint for creating tickets]` (Placeholder - *MUST BE REPLACED*)
    - **Headers:** `Content-Type: application/json`
    - **Body (JSON):**
        ```json
        {
            "assigned_to_team": "FEM Support",
            "priority": "Normal",
            "status": "Escalated by AI",
            "subject": "FEMSupport Escalation – Unresolved Issue - @{variables('varProblemSummary')}",
            "description": "User Name: @{variables('varUserName')}\nDate and Time: @{variables('varDateTime')}\nSummary of Problem: @{variables('varProblemSummary')}\nAI Response: @{variables('varAIResponse')}\nResolution Status: UNRESOLVED\nTags: @{variables('varTags')}\n\nFull Conversation Context:\n@{variables('varFullConversationContext')}",
            "custom_fields": {
                "AI_Escalation": true,
                "Conversation_Tags": "@{variables('varTags')}",
                "User_Name": "@@{variables('varUserName')}"
            }
        }
        ```
    - **Parse JSON (Optional but Recommended - after HTTP action inside this scope):**
        - Content: `Body` from the HTTP action.
        - Schema: *Generate from a sample HALO API response containing the ticket ID.*
    - **Set variable `varHaloTicketID` (after Parse JSON inside this scope):**
        - Value: *[Dynamic Content: Parsed HALO Ticket ID from Parse JSON action output]*
    - **Configure Run After:** `Scope_EmailNotification` is `Succeeded`, `has failed`, `has skipped`, `has timed out`.

**4. Scope: Log to SharePoint List (Scope_LogToSharePoint)**
    - **Action:** `Create item` (SharePoint connector)
    - **Site Address:** `[Your Fugro SharePoint Site URL]` (Placeholder - *MUST BE REPLACED, e.g., https://fugro.sharepoint.com/femsoftware*)
    - **List Name:** `FEM_Conversations`
    - **Column Mappings:**
        - `Date`: `formatDateTime(variables('varDateTime'), 'yyyy-MM-dd')`
        - `User`: `@variables('varUserName')`
        - `Summary`: `@variables('varProblemSummary')`
        - `Outcome`: "Escalated"
        - `Linked Ticket ID`: `@variables('varHaloTicketID')`
        - `Tags`: `@variables('varTags')`
    - **Configure Run After:** `Scope_CreateHALOTicket` is `Succeeded`, `has failed`, `has skipped`, `has timed out`.

**# ERROR_HANDLING_AND_COMPLETION:**
- Each major action (Email, HALO, SharePoint) is encapsulated within its own `Scope` block.
- Each subsequent `Scope` block is configured to "Run After" the preceding one has `Succeeded`, `has failed`, `has skipped`, or `has timed out`, ensuring maximum execution even if an upstream step fails.
- Consider adding a `Terminate` action at the very end of the flow to clearly indicate success or failure based on the overall outcome of the scopes.

**# NOTES:**
- Connection references for Outlook and SharePoint will need to be established or pre-configured in the Power Automate environment.
- The HALO API URI and its authentication details must be correctly configured.
- The SharePoint Site Address and the exact names of the columns in the `FEM_Conversations` list must match the environment.

BY: Michiel
