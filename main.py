def main():
    
    import json
    import os
    import sys
    import boto3

    # module_path = ".."
    # sys.path.append(os.path.abspath(module_path))
    # from utils import bedrock, print_ww


    # ---- ⚠️ Un-comment and edit the below lines as needed for your AWS setup ⚠️ ----

    # os.environ["AWS_DEFAULT_REGION"] = "<REGION_NAME>"  # E.g. "us-east-1"
    # os.environ["AWS_PROFILE"] = "<YOUR_PROFILE>"
    # os.environ["BEDROCK_ASSUME_ROLE"] = "<YOUR_ROLE_ARN>"  # E.g. "arn:aws:..."
    # os.environ["BEDROCK_ENDPOINT_URL"] = "<YOUR_ENDPOINT_URL>"  # E.g. "https://..."


    boto3_bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-west-2',
    endpoint_url='https://bedrock.us-west-2.amazonaws.com',
    )

    modelId = 'anthropic.claude-v1' # change this to use a different version from the model provider
    accept = 'application/json'
    contentType = 'application/json'

    response = boto3_bedrock.invoke_model(body=json.dumps({"prompt":"this is where you place your input text","max_tokens_to_sample":4096,"temperature":0.5,"top_k":250,"top_p":0.5,"stop_sequences":[]}),modelId="anthropic.claude-v1", accept=accept, contentType=contentType)

    prompt = """
    Please provide a summary of the following text.

    AWS took all of that feedback from customers, and today we are excited to announce Amazon Bedrock, \
    a new service that makes FMs from AI21 Labs, Anthropic, Stability AI, and Amazon accessible via an API. \
    Bedrock is the easiest way for customers to build and scale generative AI-based applications using FMs, \
    democratizing access for all builders. Bedrock will offer the ability to access a range of powerful FMs \
    for text and images—including Amazons Titan FMs, which consist of two new LLMs we’re also announcing \
    today—through a scalable, reliable, and secure AWS managed service. With Bedrock’s serverless experience, \
    customers can easily find the right model for what they’re trying to get done, get started quickly, privately \
    customize FMs with their own data, and easily integrate and deploy them into their applications using the AWS \
    tools and capabilities they are familiar with, without having to manage any infrastructure (including integrations \
    with Amazon SageMaker ML features like Experiments to test different models and Pipelines to manage their FMs at scale).

    """

    body = json.dumps({"prompt": prompt,"max_tokens_to_sample":4096,"temperature":0.5,"top_k":250,"top_p":0.5,"stop_sequences":[]})

    

    response = boto3_bedrock.invoke_model_with_response_stream(body=body, modelId=modelId, accept=accept, contentType=contentType)
    stream = response.get('body')
    output = list(stream)

    from IPython.display import display_markdown,Markdown,clear_output

    response = boto3_bedrock.invoke_model_with_response_stream(body=body, modelId=modelId, accept=accept, contentType=contentType)
    stream = response.get('body')
    output = []
    i = 1
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                chunk_obj = json.loads(chunk.get('bytes').decode())
                text = chunk_obj['completion']
                clear_output(wait=True)
                output.append(text)
                #print(''.join(text))
                display_markdown(Markdown(''.join(output)))
                i+=1
    print(''.join(output))

if __name__=="__main__":
    main()