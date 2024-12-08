load config
take photo
upload photos
tidy storage


load config:
try fetching from remote, fall back to local/hard coded values
config: how long to wait before fetching again

take photo:
if there's enough room and it's been long enough since last photo taken, take next photo, store by date
config: how frequently to take picture, max photo dir size

upload photos:
find photos in photo dir that have not been uploaded, upload and write their upload status to a file. or could have a dir of queued/uploaded.

tidy storage:
prefer deleting stuff that has been uploaded and is old.
while there is still too much stored
    if there is anything uploaded
        delete the oldest uploaded thing
    else if there is anything queued
        delete the oldest queued thing
config: headroom from the max photos dir size (could aim for it to be say 5 photos in size)


any other config?
- on/off for each step?
