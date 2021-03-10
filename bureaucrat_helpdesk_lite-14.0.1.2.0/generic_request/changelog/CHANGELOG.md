# Changelog

## Version 1.99.0

Add global setting that could be used to show/hide request statistics on kanban views of
request-related objects like Request Category, Request type, etc


## Version 1.89.0

Now requests created via xml-RPC or json RPC will get *API* channel automatically
(if not provided in creation parameters)


## Version 1.85.0

- Added new search filters for requests
    - Today
    - 24 hours
    - Week
    - Month
    - Year
- Added new group by filters for request's search view
    - Assignee
    - Is Closed
- Added request statistics (requests open/closed for today, 24h, week, etc) to
  following models:
    - Request Type
    - Request Category
    - Request Channel
    - Request Kind


## Version 1.84.0

Added *Requests* page to user form view, that is used to display request statistics for user.


## Version 1.83.0

Added button to generate default stages and route on request type that has no
request stages.


## Version 1.81.0

Added new request event types:
- Timetracking / Start Work
- Timetracking / Stop Work


## Version 1.72.0

Added new request stage type 'Progress'


## Version 1.70.0

Added new field Channel to request. The field could be used to determine source of request Website / Web / Mail / Other
Automatically set correct channels for requests created from Web and E-mail


## Version 1.68.0

Remove obsolete modules from settings page.
Obsolte modules are:
- `generic_request_action_condition`


## Version 1.67.0

Added *kanban_state* feature to requests.
Now it is possible to define additional Blocked or Ready states on request.
Also, changes of kanban state triggers event *Kanban State*


## Version 1.58.0

Merge with generic_request_timesheet module


## Version 1.56.0

Enable *create_edit* and *quick_create* features of *author* and *partner*
fields of request 


## Version 1.54.0

Added ability to assign multiple requests with a single operations.
Just select requests from list view and call context action *Assign*.


## Version 1.53.0

- Automatically move created stage to the end of list of stages.
  This is required to avoid case when new stage become first one and
  thus it become starting stage for requests.
- Better support for handling mails received from unknown contacts.
  In this case `email_from` will be saved on request
- Save `email_cc` on request (if first email contains `cc`)
- Automatically subscribe partners mentioned in ``CC`` header of incoming mail
- Implement partner suggestions for mailing for requests.
  Odoo will automatically suggest to subscribe partner and / or author of request
  if that is not following request yet


## Version 1.52.0

Use different colors for deadline icon, depending on its value.


## Version 1.47.0

Update form view of Request Type


## Version 1.46.0

Module `generic_request_tag` merged into `generic_request`


## Version 1.45.0

- Intoruced new field: *Deadline*
- Small improvements to UI
- Fixed regression, missing *Kind* field on request form view


## Version 1.44.0

Fix regression in detection of author when creator is specified directly,
but author is not specified.


## Version 1.41.0

Introduced *Request Creation Templates* feature,
that have to be used mostly by other modules to create requests with default values.


## Version 1.39.0

- Fixed bug when with incorrect display of images in request text,
  when request was created by email.
- Added `lessc` to external dependencies, to avoid confusion for users that
  have not installed `lessc` compiler. It become optional for 12.0+ installations.


## Version 1.37.0

Fix Readmore feature: update state when images (that are in request text) loaded


## Version 1.35.0

Implemented Readmore / Readless functionality for request text and request response



## Version 1.34.0

Added categories for request event types


## Version 1.32.0

- Change UI of request form view to be consistent with frontend and other places.
  This change allows to select category before request type on request creation.
- Move *Request Events* stat-buttons to separate *Technical* page


## Version 1.31.0

Added graph view for requests


## Version 1.30.0

Merge `generic_request_priority` into core (`generic_request`)


## Version 1.29.0

- Module `generic_request_kind` merged into `generic_request`
- Added demo request with long description and images
- [FIX] display of images in request body


## Version 1.28.0

- Added ability to add comment in assign wizard for request
- Added button *Assign to me* on request


## Version 1.24.0

Request name in title displayed as `h2` instead of `h1` as before


## Version 1.20.0

Add global settings:
- 'Automatically remove events older then',
- 'Event Live Time',
- 'Event Live Time Uom'


## Version 1.17.0

- Make it possible to change request category for already created request
- New request event *Category Changed*
- Show *Requests* stat-button on user's form


## Version 1.16.4

#### Version 1.16.4
Add security groups user_see_all_requests and user_write_all_requests and rules for this groups


## Version 1.16.2

#### Version 1.16.2
Added generic_request_survey to request settings list.


## Version 1.16.1

#### Version 1.16.1
Added dynamic_popover widget to description field on request tree view.


## Version 1.16.0

Added `active` field to Request Stage


## Version 1.15.6

More information in error messages


## Version 1.13.11

#### Version 1.13.11
Added the ability to include request and response texts to mail notifications.


## Version 1.13.5

#### Version 1.13.5
- Automatically subscribe request author to request


