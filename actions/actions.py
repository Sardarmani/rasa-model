from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled
from datetime import datetime, timedelta
import requests

class ActionSetReminder(Action):
    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reminder_text = tracker.get_slot('reminder_text')
        reminder_date = tracker.get_slot('reminder_date')

        # Schedule the reminder
        date_time_obj = datetime.strptime(reminder_date, '%Y-%m-%d %H:%M')
        reminder = ReminderScheduled(
            intent_name="EXTERNAL_reminder",
            trigger_date_time=date_time_obj,
            name="reminder",
            kill_on_user_message=False
        )
        
        dispatcher.utter_message(text=f"Reminder set for {reminder_date} with the message: {reminder_text}")
        return [reminder]

class ActionCancelReminder(Action):
    def name(self) -> Text:
        return "action_cancel_reminder"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Your reminder has been cancelled.")
        return [ReminderCancelled(name="reminder")]

class ActionStoreData(Action):
    def name(self) -> Text:
        return "action_store_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_data = {
            "name": tracker.get_slot('name'),
            "age": tracker.get_slot('age'),
            "state": tracker.get_slot('state'),
            "mood": tracker.get_slot('mood'),
            "mood_rating": tracker.get_slot('mood_rating'),
            "weather_impact": tracker.get_slot('weather_impact')
        }

        # Replace with your database API endpoint
        api_endpoint = "http://your-database-api.com/store_user_data"
        response = requests.post(api_endpoint, json=user_data)

        if response.status_code == 200:
            dispatcher.utter_message(text="Your data has been saved successfully.")
        else:
            dispatcher.utter_message(text="There was an error saving your data.")

        return []
