import httpx
import json

GPTJ_API = "http://api.vicgalle.net:5000/generate"


def gptj_query_simple(prompt):
    max_length = 100
    temperature = 1.0
    top_probability = 0.9
    return gptj_query(prompt, max_length, temperature, top_probability)


def gptj_query(prompt, max_length, temperature, top_probability):
    res = httpx.post(
        GPTJ_API,
        params={
            "context": prompt,
            "token_max_length": max_length,
            "temperature": temperature,
            "top_p": top_probability,
        },
    )
    data = json.loads(res.text)
    return data["text"]
