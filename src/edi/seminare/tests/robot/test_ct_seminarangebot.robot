# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.seminare -t test_seminarangebot.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.seminare.testing.EDI_SEMINARE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/seminare/tests/robot/test_seminarangebot.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Seminarangebot
  Given a logged-in site administrator
    and an add Seminarangebot form
   When I type 'My Seminarangebot' into the title field
    and I submit the form
   Then a Seminarangebot with the title 'My Seminarangebot' has been created

Scenario: As a site administrator I can view a Seminarangebot
  Given a logged-in site administrator
    and a Seminarangebot 'My Seminarangebot'
   When I go to the Seminarangebot view
   Then I can see the Seminarangebot title 'My Seminarangebot'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Seminarangebot form
  Go To  ${PLONE_URL}/++add++Seminarangebot

a Seminarangebot 'My Seminarangebot'
  Create content  type=Seminarangebot  id=my-seminarangebot  title=My Seminarangebot

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Seminarangebot view
  Go To  ${PLONE_URL}/my-seminarangebot
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Seminarangebot with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Seminarangebot title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
