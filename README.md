## Instructions to Run
- Tested on MacOS, Python 3.6
- Install requirements.txt (`pip install -r requirements.txt`)
- Run `pytest` on terminal to check unit tests against provided sample json (mixtape.json, changes.json)
- To run, execute `python mixtape.py <input.json> <changes.json> <output.json>` on terminal. Additional arguments will be ignored.

## Assumptions
- When creating a new playlist, changes.json does not contain the id (determined server-side)
- If the action requires an "existing" object, then no change should occur if the object is not found (ex. song ids that don't exist cannot be added to a playlist); we do not care about tracking these errors

## Options for Scaling
- Assuming that there can be multiple operations for a given playlist, I'd want to restructure changes.json so that changes can be processed in parallel
  - Right now, operations must be processed serially (ex. add new songs to a playlist, delete playlist)
  - If we could group changes.json into logical transactions (ex. where we'd create a playlist and then add songs to it), we could use multiple workers for executing tasks
- The way I generate new playlist ids only works for serial operations; if data fits within memory, we'd need to update the mechanism to generate the ids database side with unique index + autoincrement
- If data no longer fits within memory, we'd need to load to a database; if all the data no longer fits within a single node, we'd need to partition across multiple nodes. An option for partitioning is by id ranges, but we'd want to manage data skew as the data evolves over time.
