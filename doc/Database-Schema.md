Database Tables
===============

Outfit Table
------------

| Column Name      | Purpose |
| -----------      | ------- |
| Outfit ID        | Unique identifier for this outfit |
| Owner ID         | The facebook user ID of the owner of this outfit |
| Outfit Photo     | Serialized image associated with this outfit |



Review Table
------------

| Column Name      | Purpose |
| -----------      | ------- |
| Review ID        | UUID for a review |
| Outfit ID        | outfit ID as given in the outfit table |
| Reviewer ID      | Facebook ID of the user who owns this review |
| Rating           | {1,2,3,4,5} rating of this outfit |
| Comment          | string comment associated with this rating |
| Assigned         | whether the reviewer has gotten this review request |
| Completed        | whether the reviewer has submitted a rating and comment |

`Completed` might not be necessary, since we can allow the `rating` and
`comment` columns to be optionally null, and completed would just be checking
one of these for rating not null.
