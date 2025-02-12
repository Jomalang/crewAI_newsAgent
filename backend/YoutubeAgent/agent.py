import os
from YoutubeAgent.timecheck import time_check
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Task, Crew, Process
from YoutubeAgent.tools.transcript import TranscriptTool

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=OPENAI_API_KEY)
@CrewBase
class NewsAgent():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    transcript_tool = TranscriptTool()

    @agent
    def youtube_transcript_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["youtube_transcript_agent"],
            verbose=True,
            llm=llm,
            tools=[self.transcript_tool],
        )

    @agent
    def kor_eng_translator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['kor_eng_translator_agent'],
            verbose=True,
            llm=llm,
        )
    
    @agent
    def youtube_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["youtube_summary_agent"],
            verbose=True,
            llm=llm,
        )
    
    @task
    def youtube_transcript_task(self) -> Task:
        return Task(
            config=self.tasks_config["youtube_transcript_task"],
            expected_output="A transcript of the given youtube video.",
        )

    @task
    def kor_eng_translation_task(self) -> Task:
        return Task(
            config=self.tasks_config["kor_eng_translation_task"],
            expected_output="A translated text.",
            context=[self.youtube_transcript_task()],
        )

    @task
    def youtube_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["youtube_summary_task"],
            expected_output="A korean summary of the given translated korean text.",
            context=[self.kor_eng_translation_task()],
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential,
        )
        
@time_check
def run(inputs: dict):
    ai_agent = NewsAgent()
    crew_instance = ai_agent.crew()

    result = crew_instance.kickoff(inputs = inputs)
    return result

if __name__ == "__main__":
    run()
