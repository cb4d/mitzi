backend components are:

- a bucket. i think not even clever tiering for now. maybe should consider what that would be though.
- a user that can write to the bucket
- cloudfront for hosting the s3 static website, with basic auth for access
- the s3 static website source
