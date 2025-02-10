import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Task, Crew, Process
from timecheck import time_check

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=OPENAI_API_KEY)

@CrewBase
class NewsAgent():


    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def kor_eng_translator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['kor_eng_translator_agent'],
            verbose=True,
            llm=llm,
        )
    
    @agent
    def news_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["news_research_agent"],
            verbose=True,
            llm=llm,
        )
    
    @agent
    def news_reporting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["news_reporting_agent"],
            verbose=True,
            llm=llm,
        )
    
    @task
    def kor_eng_translation_task(self) -> Task:
        return Task(
            config=self.tasks_config["kor_eng_translation_task"],
            expected_output="A translated text."
        )
    
    @task
    def news_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["news_research_task"],
            expected_output="A list of credible sources and the information they provide.",
            context=[self.kor_eng_translation_task()]
        )

    @task
    def news_reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["news_reporting_task"],
            expected_output="A report on the latest news on the given topic to korean.",
            context=[self.news_research_task(), self.kor_eng_translation_task()],
            output_file="news_report.md"
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
def run():
    ai_agent = NewsAgent()
    crew_instance = ai_agent.crew()

    result = crew_instance.kickoff(inputs = {"topic": "nvidia_korea"})
    print(result)

if __name__ == "__main__":
    run()
