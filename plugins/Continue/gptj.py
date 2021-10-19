import httpx

GPTJ_API = "http://api.vicgalle.net:5000/generate"


async def gptj_query_simple(prompt):
    max_length = 100
    temperature = 1.0
    top_probability = 0.9
    return await gptj_query(prompt, max_length, temperature, top_probability)


async def gptj_query(prompt, max_length, temperature, top_probability):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            GPTJ_API,
            params={
                "context": prompt,
                "token_max_length": max_length,
                "temperature": temperature,
                "top_p": top_probability,
            },
        )
        data = res.json()
        return data["text"]
