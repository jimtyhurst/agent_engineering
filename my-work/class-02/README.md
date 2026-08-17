# Agent Engineering: Class 2 assignment

## Student information

[Jim Tyhurst](https://tyhurst.com)  
Repository: https://github.com/jimtyhurst/agent_engineering/

## Projects completed

1. news-highlights
2. conference-website

## Prompts used

I followed the instructions in the Codelab at https://codelabs.developers.google.com/building-with-google-antigravity for the prompts.

## Lessons learned

- I need to review carefully each implementation step.
- I needed to correct the Agent at several steps, especially when it was setting up the environment.
- When the Agent encounters an error, it is difficult to determine what is going wrong.
- On the positive side, I was surprised by the nice-looking website that was generated.

## Challenges encountered

- I was frustrated that the Agent kept trying to use my default system Python environment, even though I kept telling it to use the virtual environment that I had already created for this project.
- For some reason, the testing for `conference-website` did not work well. The Agent kept opening browser windows, but never seemed to connect to the server at http://127.0.0.1/5001 even though I was able to connect to the website when I typed that URL into a browser window. The Agent said that the connection timed out.