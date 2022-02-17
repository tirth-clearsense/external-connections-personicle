# maps google fit data types to timescaledb tables
# list all available google fit data types and map them to a personicle data type
# this mapping will keep evolving with new and custom data types

DATA_DICTIONARY = {
    # Activity data types
    "com.google.calories.bmr": "resting_calories",
    "com.google.calories.expended": "total_calories",
    "com.google.cycling.pedaling.cadence": "cycling_cadence",
    "com.google.cycling.pedaling.cumulative": "cumulative_cycling_cadence",
    "com.google.heart_minutes": "heart_intensity_minutes",
    "com.google.active_minutes": "active_minutes",
    "com.google.power.sample": "power",
    "com.google.step_count.cadence": "step_cadence",
    "com.google.step_count.delta": "step_count",
    "com.google.step_count.cumulative": "cumulative_step_count",
    # different exercise performed in a workout, should be stored as events in the personicle
    # "com.google.activity.exercise": "personal_events",
    # "com.google.activity.segment": "personal_events",

    # Body data types
    "com.google.body.fat.percentage": "body_fat_percentage",
    "com.google.heart_rate.bpm": "heart_rate",
    "com.google.height": "height",
    "com.google.weight": "weight",

    # Location data types
    "com.google.cycling.wheel_revolution.rpm": "wheel_cadence",
    "com.google.cycling.wheel_revolution.cumulative": "cumulative_wheel_cadence",
    "com.google.distance.delta": "distance_delta",
    "com.google.location.sample": "location",
    "com.google.speed": "speed",

    # Nutrition data types
    "com.google.hydration": "water_intake",
    # meal event from google fit
    # "com.google.nutrition": "food_event"

    # Sleep data types
    "com.google.sleep.segment": "sleep_stage",

    #Health data types
    "com.google.blood_glucose": "blood_glucose",
    "com.google.blood_pressure": "blood_pressure",
    "com.google.body.temperature": "body_temperature",
    "com.google.cervical_mucus": "cervical_mucus",
    "com.google.cervical_position": "cervical_position",
    "com.google.menstruation": "menstruation",
    "com.google.ovulation_test": "ovulation_test",
    "com.google.oxygen_saturation": "blood_oxygen_saturation",
    "com.google.vaginal_spotting": "vaginal_spotting"

}