# 🧠 INGESTA TÉCNICA SOTA — PROYECTO POLYDIM
**Fecha de Ingesta:** 2026-09-17 17:00:59
**Cuenta Origen:** account_cursos
**Remitente:** Daily Dose of DS <avi@dailydoseofds.com>
**Asunto:** Where does all the VRAM go during LLM inference?
**ID Correo:** 1a0b0da89271dfca

---

## 📄 PAYLOAD TÉCNICO COMPLETO:
​Master Full-stack AI Engineering ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/vqh3hrhoq2w8k5ighl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcC8= )​

----------------------
In today's newsletter:
----------------------

* Get started with all the best tools in the open AI ecosystem for free.
* ​Where does all the VRAM go during LLM inference?​
* MCP meets agent skills.

TODAY'S ISSUE

TOGETHER WITH NEBIUS
--------------------

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
​Get started with all the best tools in the open AI ecosystem for free ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/l2hehmhld5xwo5s6h0/aHR0cHM6Ly9kZXZ0b29sc2FjYWRlbXkubGluay9hdmk= )​
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

​The Nebius AI Builder Program ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/m2h7h5h3lk4wogamhq/aHR0cHM6Ly9kZXZ0b29sc2FjYWRlbXkubGluay9hdmkv ) launched last week to kickstart developers with $400+ in free credits.

With one free sign-up, developers get credits for Nebius Token Factory, Tavily, Toloka, LangSmith, and more.

​
Developers also get access to runnable cookbooks and training opportunities from some of the top companies in the industry, providing both the access and the education to get started building on the open AI ecosystem now.

For developers aiming to move into AI engineering or take an existing project beyond demos, the program provides a direct way to build production experience without paying upfront.

Things you’d learn:

* Building a deep research agent powered by Tavily and Token Factory.
* Build an agent skill for searching for car parts with Kimi K3.
* How to use OpenCode with Nebius Token Factory models.

The same learning path would otherwise require several platforms and separate resources.

Join the Nebius AI Builder Program for free at dev.nebius.com/builders ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/dpheh0he2zprqofmh4/aHR0cDovL2RldnRvb2xzYWNhZGVteS5saW5rL2F2aS8= ) and get $400+ in credits and discounts across the stack on day one.

-->​Join Nebius AI Builder Program for free ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/e0hph7h7d9r5kea8h2/aHR0cDovL2RldnRvb2xzYWNhZGVteS5saW5rL2F2aQ== )
​Join Nebius AI Builder Program for free ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/e0hph7h7d9r5kea8h2/aHR0cDovL2RldnRvb2xzYWNhZGVteS5saW5rL2F2aQ== )
Join early before it runs out.

LLMs
----

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
​Where does all the VRAM go during LLM inference? ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/owhkhqhw03q547bvhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcC9ob3ctYS1ncHUtYWN0dWFsbHktd29ya3Mv )​
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Loading the model is only the first part of the GPU memory story.

Once inference starts, VRAM is divided across model weights, the KV cache, temporary activations and workspace, and runtime overhead. Only one bucket stays roughly fixed. The others change with context length, batch size, concurrency, and model architecture.

This is why “the model fits on the GPU” and “the workload fits on the GPU” are two different statements.

The diagrams below break the memory budget into four useful buckets.

​

1. Model weights
----------------

Weights are the mostly fixed part of inference memory. A model with 8 billion parameters needs about 16 GB in FP16 or BF16, 8 GB at 8 bits per parameter, or 4 GB at 4 bits per parameter. Quantized checkpoints also store scales, zero points, and metadata.

​
The allocation does not grow during generation. Its main inputs are parameter count, numerical format, and how the model is split across GPUs.

​
Quantization also creates room for longer contexts, more simultaneous requests, or larger batches. Speed still depends on kernel support and dequantization cost, so lower precision does not guarantee higher throughput.

2. KV cache
-----------

The KV cache is the dynamic part that catches many deployments by surprise.

Each transformer layer stores key and value tensors for earlier tokens. During decoding, attention reads them instead of recomputing the full prefix at every step.

The dense-cache approximation below includes the number of active sequences. The factor of two accounts for keys and values. Grouped-query attention reduces this cost because several query heads share fewer KV heads. KV-cache quantization reduces bytes per element, with accuracy and kernel-support tradeoffs.

​
Double the cached tokens and the cache roughly doubles. Double the active sequences and it roughly doubles again. A server handling long conversations can spend more VRAM on KV state than weights.

​
Serving engines manage this memory in blocks. Paged allocation reduces waste from variable sequence lengths, while prefix caching reuses blocks when requests share an identical prompt prefix.

Some engines reserve most remaining GPU memory for this pool during startup. That reservation can make VRAM look full before real traffic arrives, even though much of the pool is still available for future tokens.

3. Activations and workspace
----------------------------

Inference needs temporary memory for layer outputs, attention, matrix multiplication, sampling, and kernel scratch space. These allocations are reused across layers, so they do not accumulate per generated token like the KV cache.

Peak size depends on the inference phase. Prefill processes prompt tokens in parallel and usually creates larger temporary tensors. Decode handles one new token per active sequence, although continuous batching can raise its footprint.

​
Different attention and matrix multiplication kernels request different workspace sizes. Memory-efficient kernels can lower the peak, while larger batches trade memory for better GPU utilization.

​
The GPU still needs enough free memory for this temporary peak. A workload can fail even when steady-state allocations appear to fit.

4. Runtime overhead
-------------------

The final bucket contains CUDA contexts, loaded kernels, communication libraries, graph captures, scheduler buffers, allocator bookkeeping, and serving-framework state.

Caching allocators keep freed blocks reserved for reuse. Reserved memory can therefore exceed live tensor memory, while nvidia-smi can report more usage than the framework’s tensor counters.

​
Fragmentation can leave enough free bytes in total but no suitable block for the next allocation. Capacity planning therefore needs headroom below the GPU’s physical limit.

​
The practical memory equation is:

Required VRAM ≈ weights + KV cache + peak activations and workspace + runtime overhead + safety margin

​
That equation explains why a model can load comfortably and still run out of memory after increasing the context window, concurrency, or batch size.

It also explains the wider performance problem. During decode, repeatedly reading weights and a growing KV cache can matter as much as raw compute capacity.

👉 Over to you: Which memory bucket has caused the most capacity problems in your inference workloads?

AGENTS
------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
​MCP meets agent skills ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0odaph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0xLw== )​
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

MCP already gave agents a standard way to connect to tools, resources, and external systems.

Now it also defines a standard way to discover and load Agent Skills directly from MCP servers.

​
The flow is simple:

→ connect to MCP server

→ discover available skills

→ inspect skill metadata

→ load the relevant 𝗦𝗞𝗜𝗟𝗟.𝗺𝗱 only when needed

​
Under the hood, Skills are served through MCP’s existing Resources primitive.

That means 𝗦𝗞𝗜𝗟𝗟.𝗺𝗱, references, scripts, examples, and other supporting files are exposed as resources that the client can read on demand.

This is especially useful for context window management.

Instead of loading every workflow instruction upfront, the agent can first discover what skills are available and pull in only the one required for the current task.

A useful mental model is:

​
* tools = what the agent can do
* resources = what the agent can access
* skills = how the agent should perform a reusable workflow

Previously, that workflow knowledge often lived separately in docs, repos, prompt files, or custom integrations.

Now the MCP server can expose the capability and the playbook for using it together.

So you get:

→ standardized skill discovery

→ on-demand context loading

→ cleaner distribution and versioning

→ reusable workflows that travel with the server

MCP was already the connection layer.

Skills now add a standardized way to ship reusable agent know-how on top of it.

The illustration below visually summarizes everything that we discussed so far.

Read more: https://github.com/modelcontextprotocol/ext-skills ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/p8heh9h4pkq899aqh3/aHR0cHM6Ly9naXRodWIuY29tL21vZGVsY29udGV4dHByb3RvY29sL2V4dC1za2lsbHM= )​

Talking about MCPs, we covered everything you need to know about MCPs in the MCP crash course.

* ​Part 1 covered MCP fundamentals, the architecture, context management, etc. → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0odaph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0xLw== )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0odaph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0xLw== )​
* ​Part 2 covered core capabilities, JSON-RPC communication, etc. → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxnwh5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0yLw== )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxnwh5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0yLw== )​
* ​Part 3 built a fully custom and local MCP client → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/dpheh0he2zprqeumh4/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0zLw== )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/dpheh0he2zprqeumh4/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0zLw== )​
* ​Part 4 built a full-fledged MCP workflow using tools, resources, and prompts → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/e0hph7h7d9r5kqc8h2/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC00Lw== )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/e0hph7h7d9r5kqc8h2/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC00Lw== )​
* ​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/7qh7h8h9xvn30zczh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC01Lw== )​Part 5 taught how to integrate Sampling into MCP workflows → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/7qh7h8h9xvn30zczh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC01Lw== )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/7qh7h8h9xvn30zczh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC01Lw== )​
* ​Part 6 covered testing, security, and sandboxing in MCP Workflows → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/owhkhqhw03q545svhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC02 )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/owhkhqhw03q545svhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC02 )​
* ​Part 7 covered testing, security, and sandboxing in MCP Workflows → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0o5cph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC03 )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0o5cph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC03 )​
* ​Part 8 integrated MCPs with the most widely used agentic frameworks: LangGraph, LlamaIndex, CrewAI, and PydanticAI → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/p8heh9h4pkq89mcqh3/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC04 )​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/p8heh9h4pkq89mcqh3/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC04 )​
* ​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxn2a5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC05Lw== )​P ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxn2a5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC05Lw== )​​​ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxn2a5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC05Lw== )​art 9 covered using LangGraph MCP workflows to build a comprehensive real-world use case→ ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/x0hph6he48qxn2a5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC05Lw== )​

THAT'S A WRAP

NO-FLUFF RESOURCES TO...
------------------------

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
​Succeed in AI Engineering roles ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/6qheh8hl3v90peuohk/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcA== )​
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

​
All businesses care about impact. That’s it!

* Can you reduce costs?
* Drive revenue?
* Can you scale ML models?
* Predict trends before they happen?

We have discussed several other topics (with implementations) in the past that align with such topics.

-->Master full-stack AI engineering ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/6qheh8hl3v90peuohk/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcA== )
Master full-stack AI engineering ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/6qheh8hl3v90peuohk/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcA== )
Here are some of them:

​
* Learn MLOps from first principles to production in this course with 18 parts → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/kkhmh6hnogx48qalh7/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWxvcHMtY3Jhc2gtY291cnNlLXBhcnQtMS8= )​
* Learn everything about MCPs in this course with 9 parts → ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/z2hghnhem9l0odaph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29udGV4dC1wcm90b2NvbC1jcmFzaC1jb3Vyc2UtcGFydC0xLw== )​
* Learn how to build Agentic systems in this course with 14 parts ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/58hvh7hg4p6l5df6h4/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYWktYWdlbnRzLWNyYXNoLWNvdXJzZS1wYXJ0LTEtd2l0aC1pbXBsZW1lbnRhdGlvbi8= ).
* Learn how to build real-world RAG apps, evaluate, and scale them in this course ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/25h2hoh3qrmn7ka3h4/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYS1jcmFzaC1jb3Vyc2Utb24tYnVpbGRpbmctcmFnLXN5c3RlbXMtcGFydC0xLXdpdGgtaW1wbGVtZW50YXRpb25zLw== ).
* Learn sophisticated graph architectures and how to train them on graph data in this course ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/g3hnh5hm07qxe0trh9/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYS1jcmFzaC1jb3Vyc2Utb24tZ3JhcGgtbmV1cmFsLW5ldHdvcmtzLWltcGxlbWVudGF0aW9uLWluY2x1ZGVkLw== ).
* So many real-world NLP systems rely on pairwise context scoring. Learn scalable approaches here ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/9qhzhnhdek5ng8t9h3/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYmktZW5jb2RlcnMtYW5kLWNyb3NzLWVuY29kZXJzLWZvci1zZW50ZW5jZS1wYWlyLXNpbWlsYXJpdHktc2NvcmluZy1wYXJ0LTEv ).
* Learn how to run large models on small devices using Quantization techniques ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/3ohphkh3k6pvqwirhn/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcXVhbnRpemF0aW9uLW9wdGltaXplLW1sLW1vZGVscy10by1ydW4tdGhlbS1vbi10aW55LWhhcmR3YXJlLw== ).
* Learn how to generate prediction intervals or sets with strong statistical guarantees for increasing trust using Conformal Predictions ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/n2hohvhvlw7e3wf6hg/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vY29uZm9ybWFsLXByZWRpY3Rpb25zLWJ1aWxkLWNvbmZpZGVuY2UtaW4teW91ci1tbC1tb2RlbHMtcHJlZGljdGlvbnMv ).
* Learn how to identify causal relationships and answer business questions using causal inference in this course ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/48hvhehm7zxkr5bxh7/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYS1jcmFzaC1jb3Vyc2Utb24tY2F1c2FsaXR5LXBhcnQtMS8= ).
* Learn how to scale and implement ML model training in this practical guide ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/wnh2hghql908wkf7hx/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vaG93LXRvLXNjYWxlLW1vZGVsLXRyYWluaW5nLw== ).
* Learn techniques to reliably test new models in production ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/reh8hohmo96n07u2h6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vNS1tdXN0LWtub3ctd2F5cy10by10ZXN0LW1sLW1vZGVscy1pbi1wcm9kdWN0aW9uLWltcGxlbWVudGF0aW9uLWluY2x1ZGVkLw== ).
* Learn how to build privacy-first ML systems using Federated Learning ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/08hwh9h2p0lqdwclh5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZmVkZXJhdGVkLWxlYXJuaW5nLWEtY3JpdGljYWwtc3RlcC10b3dhcmRzLXByaXZhY3ktcHJlc2VydmluZy1tYWNoaW5lLWxlYXJuaW5nLw== ).
* Learn 6 techniques with implementation to compress ML models ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/8ghqhoho7erklxckh9/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbW9kZWwtY29tcHJlc3Npb24tYS1jcml0aWNhbC1zdGVwLXRvd2FyZHMtZWZmaWNpZW50LW1hY2hpbmUtbGVhcm5pbmcv ).

-->Master full-stack AI engineering ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/6qheh8hl3v90peuohk/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcA== )
Master full-stack AI engineering ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/6qheh8hl3v90peuohk/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcA== )
All these resources will help you cultivate key skills that businesses and companies care about the most.

​

WORK WITH US
------------

-----------------------------------
ADVERTISE TO 950k+ AI PROFESSIONALS
-----------------------------------

Our newsletter puts your products and services directly in front of an audience that matters...thousands of leaders, senior data scientists, machine learning engineers, data analysts, etc., around the world.

Get in touch today by replying to this email.

Today’s email was brought to you by Avi Chawla and Akshay Pachaar.

​Update your profile ( https://preferences.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv ) | Unsubscribe ( https://fff97757.unsubscribe.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv )​

Looking for more? Unlock our premium DS/ML resources ( https://fff97757.click.kit-mail3.com/d0uw9gw2enc0hoxern2fmhzm5lmwptlhokgvv/vqh3hrhoq2w8k5ighl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWVtYmVyc2hpcC8= ).

​

© 2026 Daily Dose of Data Science
