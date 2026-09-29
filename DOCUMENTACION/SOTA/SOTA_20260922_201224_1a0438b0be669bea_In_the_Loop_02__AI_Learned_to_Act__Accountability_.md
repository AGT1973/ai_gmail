# 🧠 INGESTA TÉCNICA SOTA — PROYECTO POLYDIM
**Fecha de Ingesta:** 2026-09-22 20:12:24
**Cuenta Origen:** account_cursos
**Remitente:** Rasa <team@mail.rasa.com>
**Asunto:** In the Loop 02: AI Learned to Act. Accountability Didn’t Keep Up.
**ID Correo:** 1a0438b0be669bea

---

## 📄 PAYLOAD TÉCNICO COMPLETO:
Everything worth knowing in AI this month, minus the hype.

͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌

Issue 02 | September 2026

Rasa (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdq3lcq-W69sMD-6lZ3nFW3629DB4ktf6xW4Cxw2T6Zj0k5W87lm3v2lKypxW6c7jzX65BXSvN7Wyg3L32jv5W4qm9NN5J1-djF8xPZSQlH06W6D-vYl6n-4G6W9lsFxl7TmPrMW5JBDD18YnkCbW2S7Wb-7gs7VgW8sV4dS6TdlT0W7gCY1h3_ptw6W3LpbZq5RZDGxW6wMFjx18mhhgW1113g33VJXLlW2vJ_ZW25j-ygW5KmcW21Bh0hCW9khwnv25R3jZW6Q7CQr6frSRndV8yJT04 )

In the Loop

Everything worth knowing in AI this month, minus the hype

Welcome back to In the Loop, Rasa’s monthly read on what actually matters in enterprise AI.

If July was about how fast the models are moving, this month the story turned to what they’re now doing on their own. New research says AI already writes a large share of committed code that’s being shipped faster than anyone is securing it. In fact, another new report found that AI-generated code only clears security checks about 56% of the time. Meanwhile, the first wave of the EU AI Act’s transparency rules took effect, so deferring explainability is officially off the table across the EU.

The throughline? Capability has quietly moved from answering to acting, and the hard work is everything that keeps those actions accountable. That’s the same case our co-founder and CTO Alan Nichol made on stage at Ai4 this month, and it’s the lens we’re bringing to everything below.

– The Rasa Team

What we’re reading

The latest AI developments worth your attention

The EU AI Act stopped being theoretical

On August 2, the European Commission’s AI Office and national authorities began overseeing a new wave of AI Act obligations that took effect that day, including transparency requirements. Systems must now disclose when a user is interacting with AI, and AI-generated or manipulated content (including deepfakes) must be labeled and carry machine-readable marks.

Rasa’s take: For regulated buyers, this means architecture that can explain itself is now a default requirement, not an upgrade.

Read more from the European Commission
(https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfC3lcq-W8wLKSR6lZ3mFN3hd7QDQL3rKW6Q9xTq2WbwJ3W6Yq33010gC7nW8Wmgj96mPhcVW3rFczW8Sj5TcW9jwpgS5NRrgMN1Xf4ZSmh5VBW44kMbG8GhXFrW1Hj_8n4JF54DW3_xDqx6nnR05W3jbpFx5wqcglW8C1qzy7tk9JCW19wRt57q54j_W61_1X2847yCXW1LShy98Ky5D6W8GJP-B9gvzQNW4PxdMg85zrPRVk1HL75pHHLYVRM77C6VX-JhW1F5Mtp463q8ZW676V1V6r4680W5KBYkM5xZ-8gW4LxwLG18W7j8W4tLmwM22RRsDW5bN5pd3V1XqzW42kCQq8rhLC2Vq1C9B8_R3sjW3fFn-t2VJY6Mf3Lv-3g04 )

AI got better at writing code,

but it didn’t get better at securing it

Veracode’s 2026 GenAI Code Security Report found that AI-generated code passes security checks only about 56% of the time, even as the same models near-flawlessly produce code that compiles. In other words, the models have grown vastly more fluent without growing meaningfully safer while also writing more production code.

Rasa’s take: When the thing generating your code (or your agent’s next action) is right about syntax but wrong about security nearly half the time, the guardrails you put around it become fundamental.

Read more from Veracode
(https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfC3lcq-W8wLKSR6lZ3nxW6zyKpJ2F41-FW6GtJWk1zSkcdW7svpMH198DRMW40JhRP6SKq8HW8Cg-d433LM6KN4yVGG8_rNTgW1m0Bg885m05hW4gbFL06XckyXW7pxXbH2GS14bW2rmfhl9b9WpQVlFTxJ92bCvgW8kr8MX8QHwTKW1gXc_S3gTDkSW27CHPV4Y_d4KW18fB6d72_jS8VvK4jK6Mkb7sW3BMWDf57xb2gW1XLBTr94cQMKW7XhgRq9kVDLfN9c2wvLszZ4SW4bjWmr39QlglW2XHGyc5803r0W1Vh0ff5flnCWVPsrVN6GBpVbW3L9mFq7bL84mW5MtXxW4FNpthW8QrZb08B8SX9W2_wn5738yZqWf69sflj04 )

Today’s agents still fold under a well-placed prompt

Across thousands of adversarial test runs summarized by CSO Online, researchers found that indirect prompt-injection attacks succeeded against AI agents 41.7% to 68.2% of the time, and direct attacks topped 79% across every configuration tested. Every setup had at least one exploitable failure mode.

Rasa’s take: In our own red-team work with Lakera (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgf03lcq-W7lCdLW6lZ3nyW67rxYS2-PTPnW7hrq4L2fKKbKW6v2PKT6x-BZjW7DwYpn3Xwx17W2YZJRj8wDXGpW5F2G-M1rnmPCW99NBtJ219wvfW50L-lp4bm_CsW5T0Qz41bnsggW4QlkRN80Wdb7VcfL3S7fVqh9W1rKdpf3NYLHwW8MJhmC8JVXKGW7gxBXF6rcQ3lW86f2RC3B8GN6W95z9HP2LjZ19W5l4_b57JGMSQW2v3n5N5l7MldV_3Bt53_c2GQN6DCsfhvRdp7W99LXtT1wjdw2W5-wFZl19XcQ_W21bTG65_4w8hW5mHGtr8LN4q0f11ZJW-04 ) , an agent that constrains how the LLM can act held up dramatically better than a prompt-based bot asked politely to behave. Instead of trying to talk an agent out of prompt injection, design the room it moves in.

Read more from CSO Online
(https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfW3lcq-W95jsWP6lZ3psW5hZ9DZ3DDW6pW4CBJm85NHG0XW1Z0XdF1TcZy0W3pbgyS6t6ldJW1mc5tb2SpGJxW8V5GR11C_V9SW5Qf6kr5pXT2KW2xq_CQ1l9xxkW46fC6-4-3GSCW83FyZh2__LWlN7P3FhThkp3LW3hZqxp3S_glSW8-4LB48vxjVkW7zcM2Y5HRtHNW8kGB1y6wsM1XW2dfnpt417S0tW8brBfn94LZbpW3pxfNs29yywjW4-q3JY2Gx0j7VhtF4v7SNy5FVD9HZd3hVmtCW9j6dKW1f0P6CW7Pw-t44_H06mW2Jys7s2-fjmtW7X-kTy8_Tr2nVMd08R2hTN77VrQNC_1096NqW8xb4sB2B5qpNW39p9fQ5KKCS5W8FtH516571Z9f4CMf7Y04 )

Edge case

Bizarre, unexplained dispatches from the AI world

Why did an AI running a vending machine start making threats?

In Andon Labs’ Vending-Bench (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3npW6nmY2X63Y65DW3KccsK5rVwcZW9hv08P9kg4SfN5L4QVr3pSrRW1PfDvM6gLmq9W8GY-N83P0C8mW56t0hY2cFgbYW92PMdD4hK4lrN193T2Hs204YW7fftXW2WW9SXW2ZVHgp168JYCW6r_sMZ2-BnhWW5ZKfjM10tSygMm2ZrQmqXnDN3Q9XQ5PsRZVW6QHFwd5xz7vWW2hLsZg8nDG6FW6Y1b7b9j-bt9W7-rV-Y93TrlcW5rqyY57-hB2hW540zSl1B06z5W6yxc1z8DPlx3f8kM4H804 ) , frontier models ran a simulated vending machine business for a year. Claude Opus 5 set a benchmarking record with a mean final balance of roughly $11,182 (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgcR5jMY8W50kH_H6lZ3pRN80SrmhwH5MCW7-SWf18KVdJVW6Vj5g77-2t7hW3Xd-244SncFYW7m7LY88ny5h9W2zmXby2SnJ1PW6X_GxB6zPYN6W312J7j1gvvg2N2_G-wllmDVMW4wq9p08W22BsW7fD0X-1h1z7XW14xmj_8jfZt5W99Y40b14JWFXVcl6-x4nLwDzW7pl4mN3MSRxnW54lqvr97LZn8W26p6wQ4MGSczW4GLvDB6J4RLpW4572CY4cy6MFW1WBlX185qvrVW40DxFZ7VDCcjW4Dmb2c86fStRW4-lt8m3JNFxWW22dWyc7Tgs-JW23WsSM3P1lYQW5TlBM_76953hW4J59yr3YD4L7W769LyH6s4DDLW4YSNsq2Vgl86W34XYcd8ddn3cW1J67md31VFgYW3D7RVx7SSTdnf8wMY4W04 ) , but it also agreed to a price floor with a rival model, immediately undercut it by a penny, broke agreements around a dozen times, and slipped the occasional threat into its messages. It would be amusing if these weren’t the same systems we’re starting to hand real workflows…

What we’re thinking about

Expert analysis and points of view worth sitting with

Trust, not capability, is what’s slowing down agentic AI

McKinsey’s State of AI trust in 2026 (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgd65jMY8W5BWr2F6lZ3lQW4bBH3F8LjWLwMbZC95S4L_PN2P8hdrWlZbmW3D23Pd8T2p0hW197Qkt39qqJ2W8pQSnB8CdyQPW5cnq9H1N3D65Vg1BP16KdggJN75h2K62L1xWW6CwN8w5pjzMTW5nHJ2p6M7yQ5W6J7-9P1nj_nNN17vLnYZ4s27W43Vc-l7xBXYZW5MJ1GC4DWcxVW6YY0rt7PyHJLW4g6t186wx2KZW7y1V2x8l9FMxW35_j183Cz_P3W4zQL4C23QJ9DW1hCV1h84pyyMVC3G417yygMJW92YtXb2kw2RXW6bQZJ43S6mtdW1bZHGB62w7kLN7LjXXFPNDQVW2hZDS88G19HlW7lKdzW6J_19hW6X_jhb1ZRvSqW6K2jNB96lcwkW49x0H-1Y4fRfVCJJzv1sf93JVbfZP54J9fxMW3FnPM27hPkHjdHSzZg04 ) argues that the industry has entered an “agentic era” in which the binding constraint is trust, not horsepower. Security and risk are the top barriers to scaling agentic AI, and only a minority of organizations reach real maturity in responsible AI governance. The ones that do tend to see more business impact.

Agents are scaling faster than the guardrails

around them

Deloitte Insights (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfW3lcq-W95jsWP6lZ3m1W98k_RJ55mlmpW6sWvjH61MZ1kW3dk11Z2-X1JyW144kC67w10JRW4j_w5r3CBQs_W2WmZZ12Kqk1sW1QWnGm1gVLCKVrpwdd5Zw8czW80bPss2QS7YzW3Jh8P55gTz1QW5G6QVb1PCh0ZW5G8vb94qsLKTW8YJ5nv53yQP1MBSTdx5wDW5N57Lxv9j1mfBW5gYCjQ7s9-9cW4JH0QZ3xgK0mW3JBFbL1V8TV2W7M0Ywd5Q-nFTW5CDJ345qY21PW5Wd0r-4nP-nZW1d8czr44zjkgW64J4dG561j6DW6J41Pb7Ql31kW4HkB_P7c7CHPW6-8HWn3_TWy1W3RHYJB2D6yqFW1tkVmz55T43yW8QtP__1mmW44W1-0Lcx1tThJtf3FcBSz04 ) captures the AI readiness gap in one line: adoption is outrunning oversight. The analysis reports only about one in five enterprises have mature governance for agentic AI, even as a large majority expect moderate-to-extensive agent use within the next couple of years. The takeaway? Governance before scale.

There’s still no rulebook written for

autonomous agents

A research note from the Cloud Security Alliance (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfW3lcq-W95jsWP6lZ3nNW3jr6Hc4K9GF-W6zCTK84FXyJ2W9l0lBH7TMyjrW5kKQ0s3VsscdW4wc1hK8r9p6dW8rB8053PZr5wW4LvtKp2f5nzZN9gq2msf2ScWW3QJRB63S9L4kW1z-tHC888wbcVRY2-02YNXQ3W3yJK614LTxz_W5rbR4c3GcHt4N5Z4KDmGtY5ZW5VlmJN2RlmPwM9VTp9-w6RhVD-Xqr1X9Ft1W486W0m1CwZDnN4wMdMkKDW8KN9jc9FHRXXz9W3JcK7q8Cmb73W906v0j6-vtFVW42jQYT3CwNCjW2Vfwp12y48XNW5446SN8lPpmzW3Ph1463_fkHxV53_jN3Mzq-ZW1BKv0d8fKfzPW7Ryc-F2V0kL-N32LWrHRkMj3f5T9kqC04 ) points out that there’s not yet an enforceable, agent-specific security framework. The standards regulated buyers lean on (the NIST AI Risk Management Framework, ISO/IEC 42001, or even the EU AI Act) largely predate autonomous, tool-using agents. For now, the governance rests on whoever designed the system.

Rasa in the news

Where you may have spotted us this past month

Our CTO at Ai4

At Ai4 in Las Vegas, Rasa co-founder and CTO Alan Nichol made a deceptively simple argument. Every 18 or so months, language models absorb another layer of the AI stack that teams used to build by hand. The durable engineering work lives in the layer models can’t eat: context, retrieval, guardrails, and accountability.

Read Alan’s take on why the models keep eating your stack (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgf03lcq-W7lCdLW6lZ3n8V7lgQx7b7TyPN92YRwqwNd-7W6q7t3K31p7vGW69_p5d5W5jBGW83_TKf79gzxrW5Zkg8G88HnnCW33Yvcv14z2drW1W6-802bgvF7W44y5jb5Twd5sW7Sf43M1zQ_B7W1_9_Rk1ZbhhwVg2Lv42J3WPrW8txlPR4CXdY7W6Z0p3L22pV-ZW7-XyjY7tggFmW2yBGw04xbLh2W4WCgTt7wYb0ZW46r_n18KPx-ZW2LfW9M92qp5cW1rZpss7ztFGRV67R813G7NjzW6ltS962fLsxLW6dQt9s5S2MZMW6ZVM3Q4flYqSf2pb1H404 )  →

“We’re always pushing the boundary

of what people can build”

Alan also joined Genzio Media’s David Meehan at Ai4 to talk through his journey, how Rasa helps enterprises build AI agents, and why giving developers room to color outside the lines matters when you’re building AI that works for real users.

Check out a clip from the interview on X (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3mjW8jFLSS20mMsyW6fGrL57j2Qf6W49t_wf13Br5hW4tS27j5b_rlpW5BGq627JHN8wW71QbB42Df8zwW1xMcVm14STxGW8p6RF26fv_6sW6fK73F7vnYMVW6TJtPs4dpDZrW3zVhRv6C23NTW1dRvX-8b95ctVS0RnN7xZcncVZXkLs4m6TDNW5V1FXY7gp8xmW115C887p3yqNW7CgSNF3K78ytN4zF1MQcKXQSW4Z6HWG13LVBhW729X5F1yY14CN8NJyjnlZcJ9N6M1dD_yBJFFf1ClMns04 )  →

How much should we trust AI with our health?

Nevada Week asked at Ai4

Vegas PBS’s Nevada Week convened medical and AI leaders on the Ai4 floor, including the American Medical Association’s Dr. John Whyte, Dataiku’s Catalina Herrera, Credo AI’s Mike Catania, and Rasa’s Alan Nichol. They weighed the promise of AI in healthcare against the potential risks of trusting LLMs with critical health decisions.

Watch the segment on Instagram (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3lNW3c_Nzd467f7NW43lm873vSWN5W1Nqxrk1C2bhlW2VnksC5262QDW59rR077H0mffW1DZn-25lmdLZW3mRGbh4v6YcgW2QTQss2bm74wW5-7Kc15C2GXqW68rvrc7nM1MTN2b26ph6j79qV3l72P4v8P9DW1GN58M3STGqSN56mJm4QRL3QVGnTDl3N2YYyW1zz8gC1h7ql4W7RdCqp1tX7QCW32STly30VTHHW7c3j2G6Ty7F7W4Lk7DQ40B3nGW8LCCCN1vRxyDW3_0hD73TWkSwf4c9PjW04 )  →

ABBYY’s AI Pulse Podcast: What GenAI has

actually changed (and what’s hype)

On Episode 3 of ABBYY’s AI Pulse Podcast, Rasa co-founder and CTO Alan Nichol unpacked what generative AI has genuinely changed in the world, where the hype has outrun the results, and what will come next as AI agents move from answering questions to acting on them.

Listen to the full episode on YouTube (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3pfW5j841k6SXDHRN67_PH2WjVd2V50s045dFyTkW6Q7T9v39GFqJW4HV39D2cH4pFW6RfsJV40PSm-W4HK5z11thpnnW18ZwkN4dgsVMVYQdDq8_tzfwW5VKDnX2Pqq6RW8yWYn326x6dmW84CxfZ43m6XdVD1cBD3l6-1FW5wnyNR66jrtRW7ZPk0N7sGhxvW3F2rhC5nK28sVtmdFY6rXVjHW1TY6Gj3MSk4ZW7BktZL4hrhxNW3ZLZ0Q3j35N7W4FmR1B3hN253W52sZFP3GlF9Xf8gVWVg04 )  →

What Rasa is up to

Updates worth a look

Join us live:

Building Agentic AI in the Public Sector

(September 9)

Alan Nichol will sit down with José Carlos Martínez Durillo, head of the Innovative Services Department at Spain’s Agencia Estatal de Administración Digital (SGAD). They’ll discuss designing responsible agentic AI for public institutions at scale.

Register for the event here
(https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgfC3lcq-W8wLKSR6lZ3ntW1rbqtB7Jr2VMW9j24lR7KnxHnW889rjN72l7YMW625qnp8ttbzGW4YZ6yy21Y5QKW4Q_gzX8BWcYZW8sFnp72yXGdSM7H4-K9xVJ9W5V7Pk88GvqkGW7lhDd21K2bPGW1HYW_S5_9CtNW5QT8j5687fVPW2HzJXy5Mh-T4W199Kz02bzFCbW7mhv6L742lQFN2NV1Yf5sYNtW3nxzm_1Wyyj3W7pztnc3z_hL6VS3W-443cssbW4xpMrM55bg3fW89FRTp5zNPKhW1NyzpK51B8wDW2bGxSc25vytkW4rNFQ94r_zZ1V9dZ8757g0xbW1nYCfH3YLsnZW7HK3DH8-lSdRW7l4t073ky_QKf378BBb04 )

Build your next AI

agent with Rasa

Power every conversation with enterprise-grade tools that keep your teams in control.

Get a demo
(https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3nYW7cTyPx3-_vJ2W4SkSCV9ckCzNVkXcrH6Y8MGRW1V069T6BKRxTW1cXkjJ8LlLjNW4tnBjf34S8KXN4j_7nCJCRwYW3C-WGB3DfYsrW3_CprV4rZfVbW3QsNSg3sdWsqW6v7H3g4PFT1MW6F8CGv145QxyW16fDJG5H3PmjW17DDM92zHhp2N3TRvF-Hgxq2VBzjGs1vvF3KW53ZmFY66PLHNW7XQ0jJ5hcptjW8Mdd9K2zPBTjW6VCwCQ4LW89QW2x7-mb5NL8YZW8HN8jH3F0LQtf1BCWJF04 )

Rasa (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdq3lcq-W69sMD-6lZ3nFW3629DB4ktf6xW4Cxw2T6Zj0k5W87lm3v2lKypxW6c7jzX65BXSvN7Wyg3L32jv5W4qm9NN5J1-djF8xPZSQlH06W6D-vYl6n-4G6W9lsFxl7TmPrMW5JBDD18YnkCbW2S7Wb-7gs7VgW8sV4dS6TdlT0W7gCY1h3_ptw6W3LpbZq5RZDGxW6wMFjx18mhhgW1113g33VJXLlW2vJ_ZW25j-ygW5KmcW21Bh0hCW9khwnv25R3jZW6Q7CQr6frSRndV8yJT04 )

Build trustworthy AI agents

for real-world use.

GitHub (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdq3lcq-W69sMD-6lZ3lfW86PX024206pbW8PtSNp8RlnsyN7xcm6Kl3crCW5c0XyB1Mzs8xW8sJKJ16GWZPnW61_ggT9bZMC5W7BqQmM62j8GyVJ4ZwM3DYwxwW5CKHvS2zd5PXW81258H3TW7QxW4-r44F7J08tSW4V7bN05sgy1yW8LdC584qzZFsW6q7kGB1Jc4YtW5GNt622-tC-9W21vTTQ2Vn01cW5G_4_P5KNp5jW1CjwSX1S90tyW2SVm6L8s2kN1W12FYYh5C4tHBdgytdx04 )

X (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdq3lcq-W69sMD-6lZ3m5W1yhNpP4rT2KQW8D-wJF1wKy5ZW3MTxFP7r9PvgVPl7rW8ThrWfW5t9c842HfcZPW6G5cXV27vKRGW2WXhF02JRvWWW8zR9Rx1Vz182W8hmx_-7HJTVFW7mCZW45x84LHV5rZ5H9hy9d-W2jpxTq4xKBGHW3F178t604bXqW9cn7PD1NK0bJW1pX5rb45F1YXW2ZNx_y11b2QZW5GJh8W71w0ZsW7zymc18s6rVNW9j10Fg5spdshW2gVhwt2hZFb5f7xdfGb04 )

LinkedIn (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3mJW7LkqRd14-V_LW6KXdB38zW-mhW6ZCKjD91-4zWVqw51g3T0v_lW2z76JR62JX89W1r7l7_4SNdlLN2fkMwtLMq1HW5hNg6h33NG3zW4BZB0f3j50BBW2gMrX57Vp4GjW1k_9Hh48nSjkW5fTNHr6jqLSGW4lkFLZ5Ht_sJW99202V9lZ7MhW4mjdnD2zCNxMW6VRyhS2Y0nMtW3WT8jd43ZTGlW253dtD6jG7swW8m0F5p8m1lf_W4XhhdY4kcNM6W6DTmWZ2gwbT1W3yd8Ss7pV6TXf8j1H8M04 )

YouTube (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdK3lcq-W6N1vHY6lZ3kVW5QMJDH6wGdN7W2RpR4q8HBDngW6DzcDg5Ns4cCW8288yz8mRnrmW6WNjnY3zkGZGW8ldc9V5HdT50W2SxYYG22ywpKW10Sf9V4r7fNgV-3RcJ37RmjMW3BHNdN90QGX6W5Bn_NQ3KvYlPW1wn8t82f9QC-W4Cd6gM7BMYjRW4z5nVM6t3yypW5W1qb46HDvnDVPPQD37tRH2hW82g1rw7wnds-W3q3Vvv4yJjNXW2MKJw484QFs0W7cF6-r3TJCKmW5C2Scs74LTgJVRP6xk8vQqhpf3VsXSg04 )

Community (https://cPDz904.na1.hubspotlinks.com/Ctc/2L+113/cPDz904/VV-LYq33Pbb1W3xq49n2MPV62W7RdXLG5TcxwjN4CDgdq3lcq-W69sMD-6lZ3lxW72dmpK52j10BW1YmVn58LCDCCW4Z_n-N6cg9TWN7vLTSWxHSydW8QRyFy1wLFYcW2XnFxZ1_W9l7W1G2g-d5SRX7HW8gdfbm219mQMW6kCRqn3K7NzLW6RqnF_3RlXf6W8kzP5F4K_nQNW8zgngM4WN3jZW8Ps0851ncWTRW7WBbYd166lvYW4VHW3n64TxjgW1vs_CY3Vm7f-F43LKnp2nc7N4LLQtVMLFT5W8Kj6776q_0KvW7k7-GR6ZPX6Gf2K7bWW04 )

Not interested? Unsubscribe here (https://hs-6711345.s.hubspotemail.net/hs/preferences-center/en/page?data=W2nXS-N30h-zSW2PxYfh4t86WcW3_FYmP2RRWqTW4hKj0X4hqvdqW30lVbP3ZMVkTW1Sj2-24cH6tpW3CdlPk2WzQ9XW2-Dc3N1XvptdW3ZP92y3P4FfLW1Z9D4h2MnkYBW49QXD441RfkjW4tdH9-41D0wgW1VnpPd1BNDLhW4rxJnJ2YmhqyW41BmMz4r6DJFW1LgtGd4hL4YJW3GQNQ43bB-nFW3M8Y6v38kLlGW3BWsp81_rsxGW23hFkW2Hy10MW3d37zs25kTGWW2-DHbP1BsWZBW4hs7Jr41XDhzW3XP1fQ3bjCSVW2HVPGt3ZG_x1W2qCZn547L322W1Xb-3z2TgK2KW3ZVBp923qFZLW41n9v82-dWRNW2sMHLv2-fHx6W2zxQhR2zYZ-VW30JgFK2Cxg_TW1VwSrM218GVGW2CH97J47tn0TW1N7Krj3NMdWkW3R13Qw4fzBL3W2CVmTY25m4rVW3Xw1WQ49MwPkW1Bq0502xQHSvW2KpqSt4ckS51W2RMKWY4tpVNVW4plsd43yRqGSW3JKGv73zb01xW3F6GJT1-Zjv-W43TZRh3gnn7TW2-qRDd3dptNsW3_-PpL2TvqBhW2TgN_l32lLyPW3ZD3lj3C8vF0W2WtnFJ238zwyW1SCcxk2qQV9fW3jml6n1LgtMnW2FGZQf3NRrB1W3_WgJ23Fh3c-W36kr1R23j0ltW2Rg4fm2MVrHSW3DH5CZ3BV9pbW3NFxk53yWyXqW3W17zz2r7NRt0&_hsenc=p2ANqtz-_g8xF6m7DCA6_e3aCSydzeuCLZM2Nc0nKAQpl0USEtmurrjqZH4R9oyuq2la14Q5Y_bKiEK5mHA0HB1JcpJPiGQ3ZXMg&_hsmi=435581058 ) .

© Rasa Technologies Inc.. All rights reserved.

Rasa Technologies Inc., 1 Embarcadero Center Suite 1200, San Francisco CA 94111

View in browser
