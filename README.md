# LangChain Model

LangChain (prompts & LLMs) + Pydantic (data models) = LangChain Model

## 🚀 Overview

This is an easy way to populate a Pydantic model using LLMs.
Currently, this relies on OpenAI function calling, so only OpenAI can be used.
There are currently two main use cases for LangChain Models - extraction and generation.

## 📄 Installation
`pip install langchain_model`

## 💻 Usage

### Setup

First, you need to set your OpenAI key:

```python
import os
os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'
```

### Quickstart

Next, define a Pydantic model with the data schema you want to extract - and add the `langchain_model` decorator to it.

```python
from pydantic import BaseModel, Field
from langchain_model import langchain_model


@langchain_model
class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    hobbies: list[str] = Field(description="Hobbies this person enjoys")
```

Now, just pass in text and get back a populated Pydantic model!

```python
Person("Jenny (5) likes to play kickball")
```
```text
Person(name='Jenny', age=5, hobbies=['play kickball'])
```

### LLM Configuration

By default, this will use the following LLM configuration:

```python
ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

If you want to use a different configuration, you easily can!

```python
from pydantic import BaseModel, Field
from langchain_model import langchain_model
from langchain.chat_models import ChatOpenAI


@langchain_model(llm=ChatOpenAI(model="gpt-4", temperature=.5))
class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    hobbies: list[str] = Field(description="Hobbies this person enjoys")
```

### Prompt Configuration

By default, this will use the following prompt:

```python
prompt_msgs = [
    SystemMessage(
        content="You are a world class algorithm for extracting information in structured formats."
    ),
    HumanMessage(
        content="Use the given format to extract information from the following input:"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    HumanMessage(content="Tips: Make sure to answer in the correct format"),
]
default_prompt = ChatPromptTemplate(messages=prompt_msgs)
```

If you want to use a different configuration, you easily can!

```python
from pydantic import BaseModel, Field
from langchain_model import langchain_model
from langchain.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template("Make up a person that meets this criteria: {criteria}")
@langchain_model(prompt=prompt)
class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    hobbies: list[str] = Field(description="Hobbies this person enjoys")
```

You can then call this to get data in that format

```python
Person("harry potter character")
```
```text
Person(name='Hermione Granger', age=17, hobbies=['reading', 'studying', 'spellcasting'])
```

## 🔧 Use Cases

There are currently two main uses for `langchain_models` - extraction and generation.
You can control which one you use by specifying the `mode` parameter.
All this does is fetch the default prompt to use. So if you specify `mode`, you cannot also pass in a prompt.

### Extraction

This means extracting structured information from text. This is default mode of `langchain_model`,
but you can make super sure you're using this mode by using `@langchain_model(mode="extract")`.

```python
from pydantic import BaseModel, Field
from langchain_model import langchain_model


@langchain_model(mode="extract")
class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    hobbies: list[str] = Field(description="Hobbies this person enjoys")

Person("Jenny (5) likes to play kickball")
```

```text
Person(name='Jenny', age=5, hobbies=['play kickball'])
```

### Generation

This means generating structured information based on the user input.
To use this, use `@langchain_model(mode="generate")`

```python
from pydantic import BaseModel, Field
from langchain_model import langchain_model


@langchain_model(mode="generate")
class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    hobbies: list[str] = Field(description="Hobbies this person enjoys")

Person("harry potter character")
```
```text
Person(name='Harry Potter', age=17, hobbies=['Quidditch', 'Defeating Dark wizards', 'Exploring the Wizarding World'])
```
