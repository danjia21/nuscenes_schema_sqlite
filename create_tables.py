import sqlite3

conn = sqlite3.connect("nuscenes_schema.db")
cursor = conn.cursor()

conn.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS attribute (
    token TEXT PRIMARY KEY,
    name TEXT,
    description TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS calibrated_sensor (
    token TEXT PRIMARY KEY,
    sensor_token TEXT,
    translation FLOAT[3],
    rotation FLOAT[4],
    camera_intrinsic FLOAT[3][3],
    FOREIGN KEY (sensor_token) REFERENCES sensor(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS category (
    token TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    "index" INTEGER
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS ego_pose (
    token TEXT PRIMARY KEY,
    translation FLOAT[3],
    rotation FLOAT[4],
    timestamp INTEGER
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS instance (
    token TEXT PRIMARY KEY,
    category_token TEXT,
    nbr_annotations INTEGER,
    first_annotation_token TEXT,
    last_annotation_token TEXT,
    FOREIGN KEY (category_token) REFERENCES category(token),
    FOREIGN KEY (first_annotation_token) REFERENCES sample_annotation(token),
    FOREIGN KEY (last_annotation_token) REFERENCES sample_annotation(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS lidarseg (
    token TEXT PRIMARY KEY,
    filename TEXT,
    sample_data_token TEXT,
    FOREIGN KEY (sample_data_token) REFERENCES sample_data(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS log (
    token TEXT PRIMARY KEY,
    logfile TEXT,
    vehicle TEXT,
    date_captured TEXT,
    location TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS map (
    token TEXT PRIMARY KEY,
    category TEXT,
    filename TEXT
)
"""
)

# Handle the one-to-many relationship between map and logs
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS map_log (
    map_token TEXT,
    log_token TEXT,
    FOREIGN KEY (map_token) REFERENCES map(token),
    FOREIGN KEY (log_token) REFERENCES log(token),
    PRIMARY KEY (map_token, log_token)
)
"""
)


cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sample (
    token TEXT PRIMARY KEY,
    timestamp INTEGER,
    scene_token TEXT,
    next TEXT,
    prev TEXT,
    FOREIGN KEY (scene_token) REFERENCES scene(token),
    FOREIGN KEY (next) REFERENCES sample(token),
    FOREIGN KEY (prev) REFERENCES sample(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sample_annotation (
    token TEXT PRIMARY KEY,
    sample_token TEXT,
    instance_token TEXT,
    visibility_token TEXT,
    translation FLOAT[3],
    size FLOAT[3],
    rotation FLOAT[4],
    num_lidar_pts INTEGER,
    num_radar_pts INTEGER,
    next TEXT,
    prev TEXT,
    FOREIGN KEY (sample_token) REFERENCES sample(token),
    FOREIGN KEY (instance_token) REFERENCES instance(token),
    FOREIGN KEY (visibility_token) REFERENCES visibility(token),
    FOREIGN KEY (next) REFERENCES sample_annotation(token),
    FOREIGN KEY (prev) REFERENCES sample_annotation(token)
)
"""
)

# Handle the one-to-many relationship between sample_annotations and attributes
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sample_annotation_attribute (
    sample_annotation_token TEXT,
    attribute_token TEXT,
    FOREIGN KEY (sample_annotation_token) REFERENCES sample_annotation(token),
    FOREIGN KEY (attribute_token) REFERENCES attribute(token),
    PRIMARY KEY (sample_annotation_token, attribute_token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sample_data (
    token TEXT PRIMARY KEY,
    sample_token TEXT,
    ego_pose_token TEXT,
    calibrated_sensor_token TEXT,
    filename TEXT,
    fileformat TEXT,
    width INTEGER,
    height INTEGER,
    timestamp INTEGER,
    is_key_frame BOOLEAN,
    next TEXT,
    prev TEXT,
    FOREIGN KEY (sample_token) REFERENCES sample(token),
    FOREIGN KEY (ego_pose_token) REFERENCES ego_pose(token),
    FOREIGN KEY (calibrated_sensor_token) REFERENCES calibrated_sensor(token),
    FOREIGN KEY (next) REFERENCES sample_data(token),
    FOREIGN KEY (prev) REFERENCES sample_data(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS scene (
    token TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    log_token TEXT,
    nbr_samples INTEGER,
    first_sample_token TEXT,
    last_sample_token TEXT,
    FOREIGN KEY (log_token) REFERENCES log(token)
    FOREIGN KEY (first_sample_token) REFERENCES sample(token),
    FOREIGN KEY (last_sample_token) REFERENCES sample(token)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sensor (
    token TEXT PRIMARY KEY,
    channel TEXT,
    modality TEXT CHECK(modality IN ('camera', 'lidar', 'radar'))
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS visibility (
    token TEXT PRIMARY KEY,
    level TEXT,
    description TEXT
)
"""
)

conn.commit()
conn.close()
