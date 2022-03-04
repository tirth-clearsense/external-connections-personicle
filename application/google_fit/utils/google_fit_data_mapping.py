# maps google fit data types to timescaledb tables
# list all available google fit data types and map them to a personicle data type
# this mapping will keep evolving with new and custom data types

DATA_DICTIONARY = {
    # Activity data types
    "com.google.calories.bmr": "com.personicle.individual.datastream.resting_calories",
    "com.google.calories.expended": "com.personicle.individual.datastream.total_calories",
    "com.google.cycling.pedaling.cadence": "com.personicle.individual.datastream.cycling.cadence",
    "com.google.cycling.pedaling.cumulative": "com.personicle.individual.datastream.cycling.cumulative_cadence",
    "com.google.heart_minutes": "com.personicle.individual.datastream.heart_intensity_minutes",
    "com.google.active_minutes": "com.personicle.individual.datastream.active_minutes",
    "com.google.power.sample": "com.personicle.individual.datastream.cycling.power",
    "com.google.step_count.cadence": "com.personicle.individual.datastream.step.cadence",
    "com.google.step_count.delta": "com.personicle.individual.datastream.step.count",
    "com.google.step_count.cumulative": "com.personicle.individual.datastream.step.cumulative",
    # different exercise performed in a workout, should be stored as events in the personicle
    # "com.google.activity.exercise": "personal_events",
    # "com.google.activity.segment": "personal_events",

    # Body data types
    "com.google.body.fat.percentage": "com.personicle.individual.datastream.body_fat",
    "com.google.heart_rate.bpm": "com.personicle.individual.datastream.heartrate",
    "com.google.height": "com.personicle.individual.datastream.height",
    "com.google.weight": "com.personicle.individual.datastream.weight",

    # Location data types
    "com.google.cycling.wheel_revolution.rpm": "com.personicle.individual.datastream.cycling.cadence",
    "com.google.cycling.wheel_revolution.cumulative": "com.personicle.individual.datastream.cycling.cumulative_cadence",
    "com.google.distance.delta": "com.personicle.individual.datastream.distance",
    # "com.google.location.sample": "location",
    "com.google.speed": "com.personicle.individual.datastream.speed",

    # Nutrition data types
    # "com.google.hydration": "water_intake",
    # meal event from google fit
    # "com.google.nutrition": "food_event"

    # Sleep data types
    "com.google.sleep.segment": "sleep_stage",

    #Health data types
    "com.google.blood_glucose": "com.personicle.individual.datastream.blood_glucose",
    # "com.google.blood_pressure": "blood_pressure",
    # "com.google.body.temperature": "body_temperature",
    # "com.google.cervical_mucus": "cervical_mucus",
    # "com.google.cervical_position": "cervical_position",
    # "com.google.menstruation": "menstruation",
    # "com.google.ovulation_test": "ovulation_test",
    # "com.google.oxygen_saturation": "blood_oxygen_saturation",
    # "com.google.vaginal_spotting": "vaginal_spotting"

}