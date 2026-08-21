The Prompt Fingerprint provides a consistent identifier and representation that can be associated with information generated during subsequent prompt processing, including execution results, intermediate results, generated scripts or code, tool results, and other outputs.




The PF-ID and fingerprint representation are provided to the next step for association with the prompt and information generated during its processing.


################
Changes based on Director’s feedback:
We extended the flow to consider not only previous responses, but also intermediate results, generated scripts/code, tool results, and other relevant outputs from previous prompt processing. T4 was updated to maintain this historical information, T5 was updated to consider the available information when determining the appropriate processing/execution path, and T6 was updated to learn from execution outcomes, performance, cost, token usage, and user feedback to improve future prompt processing.

This captures the changes across T4 → T5 → T6 without overclaiming that T4 or T6 themselves make the reuse decision.









Recommended final wording

Process:
The system analyzes the collected information to understand how prompts and Prompt Families are being used and how useful previous information or outputs are when considered for similar prompts. It looks for patterns such as whether previous responses, intermediate results, generated scripts or code, tool results, or other outputs are useful for similar prompts, and whether using such information can reduce processing time, cost, or token usage.

The system also analyzes execution results, user feedback, model performance, and other available information to identify changes in prompt behavior. Based on these observations, it updates the Prompt Fingerprint, Prompt Family information, and other related information to support improved prompt matching and processing.

Where significant changes are identified, the system can create an updated version of the Prompt Fingerprint while retaining the earlier version for reference.







Process: The system analyzes the collected information to understand how prompts and Prompt Families are being used and how useful previous information or outputs are when considered for similar prompts. It looks for patterns such as whether previous responses, intermediate results, generated scripts or code, tool results, or other outputs are useful for similar prompts, and whether using such information can reduce processing time, cost, or token usage.

The system also analyzes execution results, user feedback, model performance, and other available information to identify changes in prompt behavior. Based on these observations, it updates the Prompt Fingerprint, Prompt Family information, and other related information to support improved prompt matching and processing.

Where significant changes are identified, the system can create an updated version of the Prompt Fingerprint while retaining the earlier version for reference.









Yes. Now let’s move to T6: Fingerprint Learning Engine.

Based on the Director’s feedback, I would make T6 slightly broader so that it learns not only from model execution results, but also from what was reused from previous executions and how useful that reuse was.

I would not introduce any new decision box here. T6 remains a learning/improvement component.

What I recommend changing

Input

Current idea is good, but we should explicitly include information about reused outputs/intermediate results.

Replace Input with:

Input: The system receives information about how prompts were processed, including Prompt Fingerprints, Prompt Families, previous responses or other reusable information, execution results, model usage, execution time, cost, token usage, cache usage, and user feedback. It may also receive information about intermediate results, generated scripts or code, tool results, and other outputs produced during prompt processing.

⸻

Process

This is where I would make the main improvement.

Replace the current Process with:

Process: The system analyzes the collected information to understand how prompts and Prompt Families are being used and how well previous information or outputs perform when reused. It looks for patterns such as which previous responses, intermediate results, generated scripts or code, tool results, or other outputs are useful for similar prompts, and whether their reuse reduces processing time, cost, or token usage.

The system also analyzes execution results, user feedback, model performance, and other available information to identify changes in prompt behavior. Based on these observations, it updates the Prompt Fingerprint, Prompt Family information, and other related information to improve future prompt matching and processing.

Where significant changes are identified, the system can create an updated version of the Prompt Fingerprint while retaining the earlier version for reference.

⸻

Output

I would also expand the output slightly to show what T6 actually produces.

Replace Output with:

Output: The system produces updated Prompt Fingerprints, refined Prompt Families, and updated information about the usefulness of previous responses, intermediate results, generated scripts or code, tool results, and other reusable outputs. It also maintains execution and usage information, such as performance, cost, token usage, and user feedback. These updates are provided back to the Prompt Identity Registry so that future prompt processing can use the accumulated information and improve over time.


Xxxxxxxxxxxxxxxxxxxxxxxxxx
T5: Inference / Execution Router

1. INPUT — change this

Your current input is already good, but it doesn’t explicitly say that T5 receives the reusable outputs we added to T4.

I recommend:

Input: The system receives the current prompt request together with the Prompt Fingerprint and associated prompt identity information retrieved from the Prompt Identity Registry (T4). This may include the Prompt Fingerprint, Prompt Family, feature representation, previous responses, intermediate results, generated scripts or code, tool results, execution history, and other associated information.

This makes it clear that T5 has access to the things that may potentially be reused.

⸻

2. PROCESS — this is the important change

Your current process starts with:

“The execution router uses the Prompt Fingerprint and the associated decisions to determine the appropriate execution path…”

Then it mainly talks about semantic cache / reusable response vs new model execution.

We need to broaden this.

I recommend replacing the current Process with:

Process: The system uses the Prompt Fingerprint and the information from previous executions to determine how the current prompt should be handled. It first checks whether useful information from a previous execution can be reused. This may include a previous response, intermediate result, generated script or code, tool result, or other output.

If suitable information is available, the system may reuse the information directly or use it as an input for processing the current prompt. This can reduce the need for a new model execution and may reduce token usage, execution time, and cost.

If suitable previous information is not available, or if it is not sufficient for the current prompt, the system performs a new model execution. The system may use the Prompt Fingerprint, Prompt Family, previous execution information, and other available information to select the appropriate model and execution settings.

During processing, the system records relevant information such as the selected model, execution result, latency, cost, token usage, whether previous information was reused, and other feedback. This information can be provided back to the Prompt Identity Registry (T4) and Fingerprint Learning Engine (T6).

⸻

3. OUTPUT — change this

Your current Output says:

“The output consists of the executed response or a reusable cached response…”

That is now too narrow because the Director specifically wants intermediate results, scripts/code, etc.

I recommend:

Output: The system produces a response using either suitable information reused from a previous execution or a newly executed model. The output may include a reused response, intermediate result, generated script or code, tool result, or newly generated response, together with the associated execution information.

The execution and reuse information is provided back to the Prompt Identity Registry (T4) for maintaining the execution history and to the Fingerprint Learning Engine (T6) for subsequent learning and refinement.





@@@@@@@@@@@@@@@@@@@@@@@@@

Process: The system checks whether the Prompt Fingerprint, or a similar fingerprint, already exists in the registry. If a matching prompt identity is found, the new prompt is linked to that existing identity. If no match is found, a new prompt identity is created.

The system stores the Prompt Fingerprint and related information, including information about previous executions and outputs produced during those executions. This may include previous responses, intermediate results, generated scripts or code, tool results, model information, and other useful outputs produced while processing the prompt.

The system can also group similar prompts into Prompt Families and keep information about how the prompts were used and performed over time. This information is made available to later processing so the system can determine whether information from a previous execution can be reused or whether a new model execution is needed.









Input

The system receives the Prompt Fingerprint, along with the information used to describe the prompt. It may also receive information from previous prompt processing, such as the model used, execution results, responses, intermediate results, generated scripts or code, cache usage, and user feedback.


Process: The system checks whether the Prompt Fingerprint, or a similar fingerprint, already exists in the registry. If a matching prompt identity is found, the new prompt is linked to that existing identity. If no match is found, a new prompt identity is created.

The system stores the Prompt Fingerprint and related information, including information about previous executions and their results. This may include previous responses, intermediate results, generated scripts or code, tool results, model information, and other useful outputs produced while processing the prompt.

The system can also group similar prompts into Prompt Families and keep information about how the prompts were used and performed over time. This information is made available to later processing so the system can determine whether information from a previous execution can be reused or whether a new model execution is needed.

Output: The system maintains a searchable Prompt Identity Repository containing Prompt Fingerprints, Prompt Families, related information, execution history, and reusable outputs from previous prompt processing. These outputs may include previous responses, intermediate results, generated scripts or code, tool results, and other execution information.

This information can be used by other parts of the system for prompt reuse, model selection, prompt optimization, security, analytics, and future learning.

₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹


Process:

The system analyzes the normalized prompt using a combination of natural language processing, machine-learning, and rule-based techniques to extract different characteristics of the prompt. The extraction may include:

1. Semantic representation – generates a semantic embedding/vector representing the overall meaning of the prompt and identifies the primary topic or subject matter.
2. Intent and task extraction – identifies the user’s requested action, such as summarization, classification, question answering, generation, comparison, or data extraction, using language-model-based classification or other intent-classification techniques.
3. Entity and concept extraction – identifies important entities, keywords, concepts, and domain-specific terms using techniques such as named-entity recognition, keyword extraction, and language-model-based information extraction.
4. Structural feature extraction – identifies instructions, constraints, conditions, number of requested outputs, expected response format, input/output requirements, and relationships between different parts of the prompt using parsing, pattern detection, or language-model-based analysis.
5. Contextual feature extraction – identifies information such as application/domain, referenced tools or APIs, attached content, conversation context, and available user or organizational metadata.
6. Operational and security feature extraction – identifies applicable security, privacy, governance, sensitivity, or execution-related attributes using rules, classifiers, or other policy-based analysis.
7. Feature normalization and consolidation – converts the extracted information into consistent representations and combines the semantic vectors, extracted attributes, classifications, structural characteristics, and contextual metadata into a unified feature representation.

The resulting feature representation provides a multi-dimensional description of the prompt and is passed to T3 for Prompt Fingerprint Generation.



Output: The system produces a structured feature representation containing the extracted semantic, intent, entity, structural, and contextual characteristics of the prompt. The representation may include semantic embeddings, extracted attributes, classifications, and associated metadata. This representation is provided to T3 for generation of the Prompt Fingerprint.
-------------------











Your T6 could therefore be

Input:
The system receives information about how prompts were handled, such as which Prompt Fingerprint and Prompt Family were used, when the request was submitted, how long the request took, how much it cost, whether a cached response was used, and any available user feedback.

Process:
The system analyzes the historical execution and feedback information associated with Prompt Fingerprints and Prompt Families. It evaluates factors such as usage patterns, execution time, cost, response outcomes, and user feedback to determine how prompts and Prompt Families are performing. Based on these patterns, the system improves Prompt Families and uses the information to make future execution decisions. Where a significant change is identified, the system can create an updated version of the Prompt Fingerprint while retaining the earlier version for reference.

Output:
The system produces updated Prompt Fingerprints, improved Prompt Families, and updated information about how each prompt can be managed, routed, and processed more effectively.








$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
The system analyzes the normalized prompt using a set of feature-extraction functions to identify key characteristics, including meaning, structure, purpose, and context. These functions parse the prompt to identify instructions, requirements, constraints, expected output, and other relevant attributes. The extracted attributes are normalized into a structured feature representation, with semantic analysis used where required to capture the meaning and relationships between prompt elements. The resulting features are used by subsequent stages of the system.







#########################
T2: Feature Extraction

Process: The system analyzes the normalized prompt using a set of feature-extraction functions to identify key characteristics, including meaning, structure, purpose, and context. These functions parse the prompt to identify instructions, requirements, constraints, expected output, and other relevant attributes. Semantic analysis may additionally be used to determine the meaning and relationships between prompt elements. The extracted characteristics are converted into a structured set of features that can be consistently used by subsequent stages of the system.








@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Innovations

1. Multi-dimensional Prompt Fingerprinting
The system creates a reusable Prompt Fingerprint by combining multiple characteristics of a prompt, including its meaning, purpose, structure, expected output, and contextual information, rather than relying only on the prompt text or a single similarity measure.

2. Persistent Prompt Identity and Prompt Families
The system maintains Prompt Fingerprints as persistent identities in a Prompt Identity Registry and associates related fingerprints into Prompt Families. This allows newly received prompts to be associated with previously known prompt identities when an appropriate relationship is identified.

3. Identity-Based Prompt Execution
The system uses the Prompt Fingerprint, Prompt Identity, and associated historical information as part of determining how a prompt should be handled and executed, including whether an existing response can be reused or whether new model execution is required.

4. Closed-Loop Learning from Prompt Execution
The system captures information from actual prompt execution and uses that information to update Prompt Fingerprints, Prompt Families, and associated historical information. The updated information is then available for subsequent prompt processing and execution.









XXXXXXXXXXXXXXXXX

Executive Summary

The invention is a method and system for creating and using a reusable digital identity for a user prompt throughout its lifecycle. When a prompt is received, the system first standardizes the prompt and identifies important characteristics such as its meaning, structure, purpose, and context. These characteristics are then combined to create a Prompt Fingerprint, which acts as a reusable identity for the prompt.

The system maintains these Prompt Fingerprints in a Prompt Identity Registry, where new prompts can be identified, related prompts can be grouped into Prompt Families, and information about previous executions can be retained. During subsequent prompt processing, the Prompt Fingerprint and its associated history can be used to determine how the prompt should be handled, including whether an existing response can be reused or whether new model execution is required. The system also captures the results of execution and uses that information to continuously improve the Prompt Fingerprints and their associated identities.

The approach therefore provides an end-to-end mechanism for identifying, organizing, reusing, executing, and continuously learning from prompts, rather than treating each prompt request as an independent interaction.

⸻

Innovations

1. Creation of a reusable Prompt Fingerprint as a digital identity

The system creates a reusable identity for a prompt by combining multiple characteristics of the prompt, rather than relying only on the original text or a single similarity value.

The Prompt Fingerprint can represent characteristics such as:

* what the user is asking,
* the meaning and topic of the request,
* how the request is structured,
* the expected type of response,
* relevant context, and
* other attributes that may affect how the prompt should be handled.

This allows prompts that are written differently but have similar meaning or purpose to be recognized and associated with one another.

⸻

2. Multi-dimensional representation of a prompt

The system represents a prompt using multiple types of information, rather than relying only on the words contained in the prompt.

For example, the system can consider:

* what the prompt means,
* what the prompt is asking the system to do,
* how the prompt is structured,
* what output is expected, and
* what contextual or operational information is associated with it.

This provides a richer representation of a prompt for subsequent identification, comparison, execution, and learning.

⸻

3. Prompt Identity Registry and Prompt Families

The system maintains a central repository that stores Prompt Fingerprints and their associated information.

When a new Prompt Fingerprint is received, the system can determine whether a corresponding or sufficiently similar prompt identity already exists.

If no suitable identity exists, the system can create a new prompt identity.

If a related identity already exists, the new request can be associated with the existing identity or Prompt Family.

This allows related prompts to be organized together and allows information from previous prompt executions to be retained and reused.

⸻

4. Using prompt identity to influence execution

The Prompt Fingerprint is not created only for identification or record keeping. The identity and associated history can be used during actual prompt execution.

The system can use the information associated with the Prompt Fingerprint to determine an appropriate execution path, including whether:

* an existing response may be reused,
* new model execution is required,
* a particular model or execution configuration should be used, or
* other applicable enterprise decisions should be applied.

This connects prompt identification with actual prompt execution.

⸻

5. Learning from actual prompt execution

The system captures information about what happens when a prompt is executed.

For example, it can record:

* which model was used,
* execution time,
* token usage,
* cost,
* whether a cache was used,
* whether execution succeeded, and
* other available feedback.

This information is associated with the Prompt Fingerprint and Prompt Family and can be used by the Fingerprint Learning Engine to improve future processing.

Thus, the Prompt Fingerprint is not static; it can evolve based on actual usage and execution experience.

⸻

6. Continuous improvement of prompt identities

The Fingerprint Learning Engine uses accumulated execution information to identify patterns and improve the representation of prompts.

For example, the system may learn that certain characteristics of a prompt are more useful for identifying related prompts or that certain execution approaches work better for a particular Prompt Family.

The resulting improvements can be incorporated back into the Prompt Identity Registry, allowing the system to continuously improve its ability to recognize, organize, reuse, and execute prompts.











&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
Step

Example 1 — New Prompt

Example 2 — Similar Older Prompt

T1: Ingestion & Normalization

Receive: “Summarize this report and identify the 3 biggest risks.” Clean and standardize the request.

Receive: “Summarize this report and list the key business risks.” Clean and standardize the request.

T2: Feature Extraction

Extract: summarization, risk identification, business report, 3 risks, expected output, etc.

Extract: summarization, risk identification, business report, key risks, expected output, etc.

T3: Fingerprint Generation

Create a fingerprint representing these characteristics.

Create a fingerprint representing these characteristics.

T4: Identity Registration

Check the registry → no matching fingerprint found → create new Prompt Identity / Family.

Check the registry → matching/similar fingerprint found → associate with existing Prompt Identity / Family.

T5: Execution Router

Use the prompt identity and available decisions to determine execution → execute the request.

Use the existing identity/history and available decisions → check for reusable response or determine execution.

T6: Learning Engine

Record the execution experience for the new identity.

Add the new execution experience to the existing identity/family and learn from previous executions.








--------------

Step

Example 1 — New Prompt

Example 2 — Similar Older Prompt


PROMPT

 "Summarize report        "Summarize report and

  and identify 3 risks"    list key business risks




T1

Receive and standardize new request

Receive and standardize similar request

T2

Identify topic, task, risks, expected output

Identify characteristics and similarity to existing prompt

T3

Generate new fingerprint PF-1001

Identify similarity to existing fingerprint PF-0520

T4

No match → create and store new identity

Match found → associate with existing identity/family

T5

No reusable answer → execute using selected model

Check for reusable answer → return cached answer or execute

T6

Learn from first execution and add history

Compare with previous executions and update history









Input:
The system receives information about how prompts were handled, such as which Prompt Fingerprint and Prompt Family were used, which model was selected, how long the request took, how much it cost, whether a cached response was used, whether the request was successful, and any available user feedback.

Process:
The system looks at this information over time to understand what works well and what does not. It identifies patterns in how different prompts and Prompt Families are handled.

Based on these patterns, the system improves how prompts are represented and grouped. It can update the importance of different prompt characteristics, improve Prompt Families, and use information such as commonly used models, performance, and user feedback to improve future decisions.

When a significant change is identified, the system can create an updated version of the Prompt Fingerprint while keeping the earlier version for reference.

Output:
The system produces updated Prompt Fingerprints, improved Prompt Families, and updated information about how prompts have performed. These updates are sent back to the Prompt Identity Registry so that future prompts can be matched, routed, and processed more effectively.








;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;(((
T5: Inference / Execution Router

Input:
The system receives the current prompt along with the Prompt Fingerprint and related information from T4. This information may include the Prompt Family, previous execution information, and other details about the prompt.

Process:
The system uses this information to decide how the prompt should be handled. It first checks whether a previous response can be reused. If not, it determines how the prompt should be processed, including which model to use and what prompt or security settings should be applied. The prompt is then sent to the selected model for processing.

During this process, the system records information such as the model used, response result, processing time, cost, token usage, and whether a cached response was used.

Output:
The system produces either a new response from the selected model or a previously stored response. It also produces information about how the prompt was processed, which can be used to update the Prompt Identity Registry and support future improvements.








₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹₹


T4: Prompt Identity Registry

Input:
The system receives the Prompt Fingerprint created in T3, along with the information used to describe the prompt. It may also receive information from later prompt processing, such as the model used, execution results, cache usage, and user feedback.

Process:
The system checks whether the Prompt Fingerprint, or a similar fingerprint, already exists in the registry. If a matching prompt identity is found, the new prompt is linked to that existing identity. If no match is found, a new prompt identity is created.

The system stores the Prompt Fingerprint and related information, such as its features, version, timestamp, and other relevant details. It can also group similar prompts into Prompt Families and keep information about how the prompts were used and performed over time.

Output:
The system maintains a searchable Prompt Identity Repository containing Prompt Fingerprints, Prompt Families, related information, and execution history. This information can be used by other parts of the system for prompt reuse, model selection, prompt optimization, security, analytics, and future learning.








///////////












T3: Prompt Fingerprint Generation

Input:
The system receives the features identified in T2, including information about the prompt’s meaning, structure, context, security information, and other related details.

Process:
The system uses these features to create a Prompt Fingerprint that represents the prompt. It combines information about the prompt’s meaning, structure, and context to create a representation that can be used to recognize the prompt later. The system may also generate additional information, such as a confidence score and a complexity or risk score.

Output:
The system produces a Prompt Fingerprint Identifier (PF-ID) along with the fingerprint representation and related information, such as the feature summary, confidence score, and complexity or risk score. The Prompt Fingerprint is then provided to T4: Prompt Identity Registry for storage and management.















Input:
The system receives the cleaned and standardized prompt from T1, along with any related files, conversation information, and other information associated with the prompt.

Process:
The system examines the prompt to understand three main things:

* Meaning: What the prompt is asking for, including its intent, topics, and important entities.
* Structure: How the prompt is written, including instructions, requirements, restrictions, complexity, and the expected type of answer.
* Context: Information about the situation in which the prompt is being used, such as the business area, required capabilities, tools or APIs, input or output requirements, and security-related information.

The system combines these characteristics into a single representation of the prompt.

Output:
The system produces a combined set of features describing the prompt’s meaning, structure, and context.




@@@@@@@@@@@@&@&@&&&'km
Input:
The system receives the user’s prompt along with any related files, images, conversation history, tool information, and other information available with the request.

Process:
The system collects all the information related to the prompt and puts it into a common format. It removes unnecessary differences such as extra spaces, formatting, or other variations while keeping the original meaning of the prompt unchanged.

Output:
The system produces a cleaned and standardized version of the prompt, together with the related information. This becomes the input for the next step






------






Use two scenarios throughout the entire architecture

Example 1 — New Prompt

“Summarize the attached quarterly financial report into five key findings and highlight any significant changes from the previous quarter.”

Assume this prompt has never been seen before.

Example 2 — Existing / Similar Prompt

“Summarize the attached quarterly financial report into five key findings and highlight the major changes from the previous quarter.”

Assume a semantically similar prompt and its Prompt Fingerprint already exist in the registry.

⸻

How the examples should appear beside each T box

For example, beside T1, we can have:

Example 1 — New Prompt

User submits a new prompt with an attached financial report. T1 ingests the prompt, attachment, conversation context and metadata, and normalizes the request.

Example 2 — Existing / Similar Prompt

User submits a prompt with the same objective as a previously processed request. T1 performs the same ingestion and normalization; at this stage, it does not yet determine whether the prompt is new or existing.

That last point is important: T1 shouldn’t say it knows the prompt is old/new. That determination happens later.

⸻

Then T2

Example 1 — New Prompt

T2 extracts semantic, structural and contextual features from the normalized request, such as summarization intent, financial-report domain, five-item output requirement and comparison requirement.

Example 2 — Existing / Similar Prompt

T2 extracts the corresponding features. Although the wording may differ slightly from the previously processed prompt, the resulting feature representation may be highly similar.

⸻

T3

Example 1 — New Prompt

T3 converts the extracted features into a Prompt Fingerprint and generates a new PF-ID.

Example 2 — Existing / Similar Prompt

T3 generates a Prompt Fingerprint for the current request. The fingerprint can subsequently be compared with fingerprints already stored in the registry.

⸻

T4 — this is where the paths become interesting

Example 1 — New Prompt

T4 finds no equivalent or sufficiently similar Prompt Fingerprint. A new Prompt Identity and, where applicable, a new Prompt Family are created and registered.

Example 2 — Existing / Similar Prompt

T4 identifies an equivalent or semantically similar Prompt Fingerprint already registered in the repository and associates the current request with the existing Prompt Identity and Prompt Family.

This is probably the most important example in the entire diagram, because it demonstrates why the Prompt Identity Registry exists.

⸻

T5

Then both examples can converge again.

Example 1 — New Prompt

T5 uses the newly registered Prompt Identity and available execution decisions to determine the appropriate execution path, model and parameters, and executes the request.

Example 2 — Existing / Similar Prompt

T5 uses the existing Prompt Identity, historical execution information and applicable decisions to determine whether a cached response can be reused or whether model execution is required.

⸻

T6

Example 1 — New Prompt

T6 receives the execution results and operational feedback, evaluates the performance of the new Prompt Fingerprint and updates the associated identity and feature information.

Example 2 — Existing / Similar Prompt

T6 uses the accumulated execution history of the existing Prompt Identity and Prompt Family to identify performance patterns and refine feature weights, family relationships or fingerprint versions.




===€€€€$$$$<<<]££€€]++%%%]+==========
The input consists of the current prompt request together with the Prompt Fingerprint and associated prompt identity information retrieved from the Prompt Identity Registry (T4). This may include the Prompt Fingerprint, Prompt Family, feature representation, execution history, and associated metadata required for execution decisioning.





T5: Inference / Execution Router

Input

The input consists of the current prompt request together with the Prompt Fingerprint and associated prompt identity information retrieved from the Prompt Identity Registry (T4). This may include the Prompt Fingerprint, Prompt Family, feature representation, execution history, and decisions or recommendations generated by applicable downstream services, such as semantic caching, model selection, prompt optimization, security and governance, or LLM-as-a-Judge.

Process

The execution router uses the Prompt Fingerprint and the associated decisions to determine the appropriate execution path for the incoming prompt. It first evaluates whether a reusable response is available through semantic cache or whether the prompt requires new model execution. When execution is required, the router applies the applicable model-selection, prompt-optimization, security, governance, and other decisioning outcomes to determine the appropriate model, prompt configuration, and execution parameters. The resulting request is then routed to the selected model or model set for inference.

During execution, the router captures relevant operational information, including the selected model, execution outcome, latency, cost, token usage, cache status, and other feedback required for updating the Prompt Identity Registry and supporting the Fingerprint Learning Engine.

Output

The output consists of the executed response or a reusable cached response, together with the associated execution outcome and operational metadata. The execution information is provided back to the Prompt Identity Registry for maintaining execution history and to the Fingerprint Learning Engine for subsequent learning and refinement.


==================================

The input consists of the consolidated feature representation and associated metadata generated by T2, together with the Prompt Fingerprint generated by T3. The Prompt Fingerprint includes the Prompt Fingerprint Identifier (PF-ID), fingerprint vector or signature, feature summary, confidence score, complexity or risk score, and associated prompt metadata. In addition, execution-related information generated during subsequent prompt processing, including model selection, execution metrics, cache utilization, and user feedback, is received to enrich the stored prompt identity and its execution history.








The normalized prompt and associated metadata are analyzed to derive a comprehensive set of features that characterize the prompt beyond its raw textual representation. The extraction process identifies three primary categories of features: semantic features that capture the meaning, intent, entities, and topics of the prompt; structural features that capture how the prompt is constructed, including its instructions, constraints, complexity, and expected output format; and contextual features that capture the operational context, such as the applicable domain, required capabilities, referenced tools or APIs, input/output requirements, and security attributes.

The extracted features are then consolidated into a unified feature representation that preserves the different dimensions of the prompt. This representation provides a richer characterization than semantic information alone and is subsequently made available to the downstream fingerprint generation and prompt identity registration stages.



OUTPUT

The output is a consolidated feature representation containing the semantic, structural, and contextual characteristics of the prompt, together with the associated metadata. This representation is provided to the downstream fingerprint generation and prompt identity registration stages, supporting the generation of the Prompt Fingerprint (PF-ID) and the registration and management of the corresponding prompt identity.





The normalized prompt and associated metadata are analyzed to derive a comprehensive set of features that characterize the prompt beyond its raw textual representation. The extraction process identifies three primary categories of features: semantic features that capture the meaning, intent, entities, and topics of the prompt; structural features that capture how the prompt is constructed, including its instructions, constraints, complexity, and expected output format; and contextual features that capture the operational context, such as the applicable domain, required capabilities, referenced tools or APIs, input/output requirements, and security attributes.

The extracted features are then consolidated into a unified feature representation that preserves the different dimensions of the prompt. This representation provides a richer characterization than semantic information alone and is subsequently used by T3 for generating the Prompt Fingerprint.



The normalized prompt and associated metadata are analyzed to extract three categories of features: semantic features representing the meaning and intent of the prompt, structural features representing its composition, instructions, constraints, and expected output format, and contextual features representing its domain, required capabilities, referenced tools or APIs, input/output requirements, and applicable security attributes. The extracted features are consolidated into a unified representation of the prompt.




The Prompt Ingestion and Normalization module receives an incoming prompt request intercepted from the GenAI application or LLM interaction layer before execution by the target LLM. The input may consist of textual prompts, uploaded documents, files, images, or other multimodal content, together with associated conversation history, system or tool metadata, and user or organizational metadata. These inputs collectively represent the request and its execution context that are made available to the Prompt Fingerprinting System for subsequent feature extraction and fingerprint generation.







-- =========================================
-- TABLE T1 (PARENT TABLE)
-- 15 PRIMARY KEYS
-- =========================================

CREATE TABLE T1 (
    col1 INT PRIMARY KEY
);

INSERT INTO T1 VALUES
(1),(2),(3),(4),(5),
(6),(7),(8),(9),(10),
(11),(12),(13),(14),(15);

-- =========================================
-- TABLE T2 (CHILD TABLE)
-- col2 is foreign key referencing T1.col1
-- =========================================

CREATE TABLE T2 (
    col1 INT,
    col2 INT,
    FOREIGN KEY (col2) REFERENCES T1(col1)
);

INSERT INTO T2 VALUES
(101,1),
(102,1),
(103,2),
(104,3),
(105,3),
(106,3),
(107,7),
(108,10),
(109,15);










data = [

    (1, "HR", 5000),

    (2, "HR", 7000),

    (3, "IT", 6000),

    (4, "IT", None),

    (5, "IT", 8000)

]

columns = ["emp_id", "dept_id", "salary"]

df = spark.createDataFrame(data, columns)

df.show()



import ctypes
import random
import time

user32 = ctypes.windll.user32

# Mouse event constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Keyboard constants
VK_TAB = 0x09
VK_MENU = 0x12   # ALT key

# Screen size
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def move_mouse_slightly():
    x = random.randint(200, screen_width - 200)
    y = random.randint(200, screen_height - 200)

    user32.SetCursorPos(x, y)

def press_alt_tab():
    # ALT down
    user32.keybd_event(VK_MENU, 0, 0, 0)

    # TAB press
    user32.keybd_event(VK_TAB, 0, 0, 0)
    user32.keybd_event(VK_TAB, 0, 2, 0)

    # ALT up
    user32.keybd_event(VK_MENU, 0, 2, 0)

def harmless_right_click():
    # Right click at current position
    user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def press_shift():
    VK_SHIFT = 0x10
    user32.keybd_event(VK_SHIFT, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_SHIFT, 0, 2, 0)

print("Running human-like activity simulation...")

while True:
    action = random.choice([
        "move",
        "move",
        "move",
        "shift",
        "right_click",
        "alt_tab"
    ])

    if action == "move":
        move_mouse_slightly()
        print("Mouse moved")

    elif action == "shift":
        press_shift()
        print("Shift pressed")

    elif action == "right_click":
        harmless_right_click()
        print("Right click")

    elif action == "alt_tab":
        press_alt_tab()
        print("Alt+Tab pressed")

    # Random wait between actions
    wait_time = random.randint(20, 90)
    print(f"Waiting {wait_time} seconds...\n")

    time.sleep(wait_time)






from concurrent.futures import ThreadPoolExecutor
import os

files = []

for root, dirs, filenames in os.walk(VAR_SOURCE):
    for f in filenames:
        files.append(os.path.join(root, f))

def upload(file):
    dest = file.replace(VAR_SOURCE, VAR_DESTINATION)
    s3.put(file, f"s3://{dest}")

with ThreadPoolExecutor(10) as ex:
    list(ex.map(upload, files))
    









from concurrent.futures import ThreadPoolExecutor
import os

files = []

for root, dirs, filenames in os.walk(VAR_SOURCE):
    for f in filenames:
        files.append(os.path.join(root, f))

def upload(file):
    dest = file.replace(VAR_SOURCE, VAR_DESTINATION)
    s3.put(file, dest)
    return file

with ThreadPoolExecutor(8) as executor:
    list(executor.map(upload, files))












from google.cloud import storage

client = storage.Client()
bucket = client.bucket("prod-corp-pyfarm-amrm-a18d-k104630")

blob = bucket.blob("test/hello.txt")
blob.delete()

print("Deleted successfully")






bucket = client.bucket("prod-corp-pyfarm-amrm-a18d-k104630")

blobs = list(bucket.list_blobs())

print([b.name for b in blobs[:20]])


from google.cloud import storage

client = storage.Client()
bucket = client.bucket("prod-corp-pyfarm-amrm-a18d-k104630")

blob = bucket.blob("test/hello.txt")
blob.upload_from_string("Hello from Pyfarm!")

print("Uploaded successfully")




Apply scalable clustering on embeddings using distributed frameworks:

• Distributed K-Means (e.g., Spark MLlib) for large-scale clustering  
• Mini-batch K-Means for memory-efficient processing  
• FAISS (GPU-accelerated) for fast similarity-based clustering  
• Optional: Density-based methods (DBSCAN / HDBSCAN) for irregular patterns  

Distributed Execution:
• Partition embeddings across compute nodes  
• Parallel computation of distances and centroid updates  
• Iterative refinement of clusters across workers  


Other wordings

Employ a clustering approach on embedding representations to group 
transactions based on similarity in the embedding space.

Clustering may be performed using:
• Direct clustering on high-dimensional embeddings (e.g., K-Means)
• Dimensionality reduction followed by clustering:
  – PCA for scalable linear reduction
  – t-SNE / UMAP for non-linear projection (e.g., visualization or exploratory analysis)

For large-scale datasets, clustering may be implemented in a distributed manner:
• Partition embeddings across compute nodes
• Perform parallel distance computations and centroid updates
• Use distributed frameworks (e.g., Spark MLlib) or vector search systems (e.g., FAISS)








(New Section)

🔷 Add a NEW BOX after clustering:

“Scoring New Observations (Cluster Assignment & Risk Scoring)”


Input

New transaction data processed into embedding representation using the trained model

Process

Assign the new transaction to an existing cluster based on similarity in embedding space.

Cluster assignment may be performed by:
• Computing distance to cluster centroids (e.g., nearest centroid assignment)
• Using nearest-neighbor search against clustered embeddings (e.g., FAISS)
• Applying trained clustering models (e.g., K-Means predict step)

Compute a risk score using:
• Cluster-level statistics (e.g., fraud rate of assigned cluster)
• Distance-based measures (e.g., distance to fraud centroid or nearest fraud instance)
• Model prediction probability

In distributed environments:
• Broadcast cluster centroids to scoring nodes
• Perform parallel similarity computations for real-time or batch scoring


Output

Assigned cluster ID and associated risk score for the new transaction


The assigned cluster and associated metrics enable identification of potential anomalies or fraud in incoming transactions.




Ways to Update Clustering with Streaming Data

🔷 1. Incremental (Online) K-Means — ⭐ Recommended

🔹 How it works:
	•	Each new transaction:
	1.	Assign to nearest cluster
	2.	Update centroid slightly
  
  
2. Mini-Batch Updates (Streaming Batches)

🔹 How it works:
	•	Collect small batch (e.g., 1000 transactions)
	•	Update clusters periodically

🔷 3. Periodic Re-Clustering (Hybrid Approach) — ⭐ MOST PRACTICAL

🔹 Strategy:
	•	Real-time: assign to clusters
	•	Periodically (daily/weekly):
	•	Recompute clusters fully


🔷 4. Streaming Clustering Frameworks

Options:
	•	Spark Structured Streaming + MLlib
	•	River (online ML library)
	•	Flink ML












common_cols = ['account_id', 'fraud_tag', 'amount']

raw_small = raw_df[common_cols + ['feature1', 'feature2']].copy()

raw_small['_row_id'] = raw_small.groupby(common_cols).cumcount()
df2['_row_id'] = df2.groupby(common_cols).cumcount()

result = df2.merge(
    raw_small,
    on=common_cols + ['_row_id'],
    how='left'
).drop(columns=['_row_id'])


import subprocess

# Run first script
print("Running run_1.py...")
result1 = subprocess.run(["python", "run_1.py"])

if result1.returncode != 0:
    print("run_1.py failed. Stopping execution.")
    exit(1)

# Run second script only after first completes
print("Running run_2.py...")
result2 = subprocess.run(["python", "run_2.py"])

if result2.returncode != 0:
    print("run_2.py failed.")
else:
    print("Both scripts completed successfully.")











from concurrent.futures import ProcessPoolExecutor, as_completed

if __name__ == "__main__":
    start_time = time.time()
    inputs = list(range(1201, 1401))

    results = []

    with ProcessPoolExecutor(max_workers=26) as ex:
        futures = {ex.submit(safe_process, i): i for i in inputs}

        for future in as_completed(futures):
            file_id = futures[future]
            try:
                res = future.result()
                if res is not None:
                    results.append(res)
            except Exception as e:
                print(f"FAILED file {file_id}: {e}")

    end_time = time.time()
    duration = end_time - start_time

    print(f"Time taken: {int(duration // 60)} min {duration % 60:.2f} sec")




import optuna
import xgboost as xgb
import joblib

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


# -------------------------------
# Train / Validation Split
# -------------------------------

X_tr, X_val, y_tr, y_val = train_test_split(
    X_train_base,
    y_train_base,
    test_size=0.2,
    stratify=y_train_base,
    random_state=42
)


# -------------------------------
# Optuna Objective
# -------------------------------

def objective(trial):

    params = {

        "objective": "binary:logistic",
        "eval_metric": "auc",

        "tree_method": "hist",
        "enable_categorical": True,

        "max_depth": trial.suggest_int("max_depth", 4, 10),

        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.05, log=True),

        "n_estimators": trial.suggest_int("n_estimators", 300, 1200),

        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),

        "subsample": trial.suggest_float("subsample", 0.7, 1.0),

        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),

        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10, log=True),

        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10, log=True),

        "scale_pos_weight": trial.suggest_float("scale_pos_weight", 5, 150),

        "n_jobs": -1
    }

    model = xgb.XGBClassifier(**params)

    model.fit(
        X_tr,
        y_tr,
        eval_set=[(X_val, y_val)],
        early_stopping_rounds=50,
        verbose=False
    )

    preds = model.predict_proba(X_val)[:,1]

    auc = roc_auc_score(y_val, preds)

    return auc


# -------------------------------
# Run Optimization
# -------------------------------

study = optuna.create_study(direction="maximize")

study.optimize(objective, n_trials=50)


print("Best AUC:", study.best_value)

print("Best Params:", study.best_params)


# -------------------------------
# Train Final Model
# -------------------------------

best_params = study.best_params

final_model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="auc",
    tree_method="hist",
    enable_categorical=True,
    **best_params
)

final_model.fit(X_train_base, y_train_base)


# -------------------------------
# Save Model
# -------------------------------

model_path = "/nas/pyfrm_dev_3/k104630/model_run_data/6-months-data/model_xgb_run/xgb_optuna_model.joblib"

joblib.dump(final_model, model_path)

print("Model saved to:", model_path)












eval_df = pd.DataFrame({
    "y_true": y_test_base,
    "score": y_prob
})

eval_df = eval_df.sort_values("score", ascending=False)

total_fraud = eval_df["y_true"].sum()

for pct in [0.01, 0.03, 0.05]:
    
    top_k = int(len(eval_df) * pct)
    
    captured = eval_df.head(top_k)["y_true"].sum()
    
    print(f"Top {int(pct*100)}% Capture:",
          captured / total_fraud)



import xgboost as xgb
import joblib

final_model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="auc",

    subsample=1.0,
    scale_pos_weight=7.475275434670339,
    reg_lambda=5,
    reg_alpha=10,
    n_estimators=360,
    min_child_weight=3,
    max_depth=7,
    learning_rate=0.02,
    colsample_bytree=1
)

final_model.fit(X_train_base, y_train_base)


joblib.dump(
    final_model,
    "/nas/pyfrm_dev_3/k104630/model_run_data/6-months-data/model_xgb_run/base_line_model_6_months_train.joblib"
)


model = joblib.load("base_line_model_6_months_train.joblib")

proba = model.predict_proba(X_test)[:,1]

pred = model.predict(X_test)







import os
import re

files = [
    os.path.join(TRAIN_PATH, f)
    for f in os.listdir(TRAIN_PATH)
    if f.endswith(".parquet")
]

files = sorted(
    files,
    key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group())
)

sampled_dfs = []

for f in files:
    df = pd.read_parquet(f)
    df_sample = df.sample(frac=0.1, random_state=42)
    sampled_dfs.append(df_sample)

raw_train_df = pd.concat(sampled_dfs, ignore_index=True)

print(raw_train_df.shape)

print(raw_train_df[target_col].value_counts())
print(raw_train_df[target_col].value_counts(normalize=True))






import pandas as pd
import os

files = [
    os.path.join(TRAIN_PATH, f)
    for f in os.listdir(TRAIN_PATH)
    if f.endswith(".parquet")
]

sampled_dfs = []

for f in files:
    df = pd.read_parquet(f)
    df_sample = df.sample(frac=0.1, random_state=42)
    sampled_dfs.append(df_sample)

raw_train_df = pd.concat(sampled_dfs, ignore_index=True)

print(raw_train_df.shape)










import pandas as pd
import os

files = [os.path.join(TRAIN_PATH, f) for f in os.listdir(TRAIN_PATH)]

raw_train_df = pd.DataFrame()

for f in files:
    df = pd.read_parquet(f)
    df_sample = df.sample(frac=0.1, random_state=42)
    raw_train_df = pd.concat([raw_train_df, df_sample], ignore_index=True)

print(raw_train_df.shape)












X_train_base = train_base.drop(columns=[target_col])
y_train_base = train_base[target_col]

obj_cols = X_train_base.select_dtypes(include=["object"]).columns

X_train_base[obj_cols] = X_train_base[obj_cols].fillna("missing")

for c in obj_cols:
    X_train_base[c] = X_train_base[c].astype("category")


print(X_train_base.select_dtypes(include=['object']).columns)

print(X_train_base.select_dtypes(include=['category']).shape)



import pyautogui
import mss
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2_vl_7b-instruct"

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)

model = AutoModelForVision2Seq.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save("screen.png")
        return img


def ask_model(image):

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": """
Look at this computer screenshot.

Identify a button that can be clicked and return coordinates.

Respond in JSON:
{ "action": "CLICK", "x": ?, "y": ? }
"""}
            ]
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[image],
        padding=True,
        return_tensors="pt"
    ).to("cuda")

    output = model.generate(**inputs, max_new_tokens=200)

    return processor.decode(output[0], skip_special_tokens=True)


while True:

    img = capture_screen()

    response = ask_model(img)

    print(response)

    break






###################

from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2_vl_7b-instruct"

processor = AutoProcessor.from_pretrained(
    model_path,
    use_fast=True,
    trust_remote_code=True
)

model = AutoModelForVision2Seq.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

image = Image.open("/commons/users/k104630/test-image/test-image.png")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Describe this image"}
        ]
    }
]

text = processor.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = processor(
    text=[text],
    images=[image],
    padding=True,
    return_tensors="pt"
).to("cuda")

output = model.generate(**inputs, max_new_tokens=100)

print(processor.decode(output[0], skip_special_tokens=True))




from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2_vl_7b-instruct"

processor = AutoProcessor.from_pretrained(
    model_path,
    use_fast=True,
    trust_remote_code=True
)

model = AutoModelForVision2Seq.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

# example image path
image = Image.open("/apps/dli_test/test.png")

inputs = processor(
    images=image,
    text="Describe this image",
    return_tensors="pt"
).to("cuda")

output = model.generate(**inputs, max_new_tokens=100)

print(processor.decode(output[0], skip_special_tokens=True))













#=====MIN DISTANCE TO ANY FRAUD======


import numpy as np

# Select cluster
cluster_id = 4

dfw_c4 = dfw_tSNE[dfw_tSNE['cluster'] == cluster_id]

fraud_idx = dfw_tSNE[
    (dfw_tSNE['cluster'] == cluster_id) &
    (dfw_tSNE['label'] == 1)
].index

nonfraud_idx = dfw_tSNE[
    (dfw_tSNE['cluster'] == cluster_id) &
    (dfw_tSNE['label'] == 0)
].index



fraud_embeddings = embeddings_raw[fraud_idx]
nonfraud_embeddings = embeddings_raw[nonfraud_idx]

# Compute pairwise distances (NonFraud x Fraud)
# shape will be (num_nonfraud, num_fraud)

dist_matrix = np.linalg.norm(
    nonfraud_embeddings[:, None, :] - fraud_embeddings[None, :, :],
    axis=2
)

# For each non-fraud, get minimum distance to any fraud
min_distances = dist_matrix.min(axis=1)


df_c4_nfraud = dfw_c4[dfw_c4['label'] == 0].copy()

df_c4_nfraud['min_distance_to_any_fraud'] = min_distances


df_c4_min_suspicious = df_c4_nfraud.sort_values(
    ['min_distance_to_any_fraud', 'probs'],
    ascending=[True, False]
)

df_c4_min_suspicious.head(20)



#=====MIN DISTANCE TO ANY FRAUD======






fraud_75 = np.percentile(fraud_distances, 75)

inside_fraud_core = (
    df_c4_centroid_suspicious['distance_to_fraud_center'] <= fraud_75
).sum()

print("Non-fraud inside fraud 75% radius:", inside_fraud_core)
print("Percentage:", inside_fraud_core / len(df_c4_centroid_suspicious))








fraud_distances = np.linalg.norm(
    fraud_embeddings - fraud_centroid, axis=1
)

print("Fraud distance describe:")
print(pd.Series(fraud_distances).describe())

print("\nSuspicious non-fraud distance describe:")
print(df_c4_centroid_suspicious['distance_to_fraud_center'].describe())






print("Fraud avg distance to centroid:",
      np.mean(np.linalg.norm(fraud_embeddings - fraud_centroid, axis=1)))

print("Non-fraud avg distance:",
      df_c4_centroid_suspicious['distance_to_fraud_center'].mean())






# Get indices from dataframe
fraud_idx = dfw_tSNE[
    (dfw_tSNE['cluster'] == 4) & 
    (dfw_tSNE['label'] == 1)
].index

nonfraud_idx = dfw_tSNE[
    (dfw_tSNE['cluster'] == 4) & 
    (dfw_tSNE['label'] == 0)
].index




fraud_embeddings = embeddings_raw[fraud_idx]
nonfraud_embeddings = embeddings_raw[nonfraud_idx]



fraud_centroid = fraud_embeddings.mean(axis=0)



import numpy as np

distances = np.linalg.norm(
    nonfraud_embeddings - fraud_centroid,
    axis=1
)



df_c4_nfraud = dfw_c4[dfw_c4['label'] == 0].copy()

df_c4_nfraud['distance_to_fraud_center'] = distances


df_suspicious = df_c4_nfraud.sort_values(
    ['distance_to_fraud_center', 'probs'],
    ascending=[True, False]
)

df_suspicious.head(20)

















import numpy as np

# Fraud embeddings in cluster 4
fraud_mask = (df_c4['label'] == 1)
fraud_embeddings = embeddings_sub[(cluster_ids == 4) & (labels_sub == 1)]

fraud_centroid = fraud_embeddings.mean(axis=0)

# Non-fraud embeddings
nonfraud_embeddings = embeddings_sub[(cluster_ids == 4) & (labels_sub == 0)]

distances = np.linalg.norm(nonfraud_embeddings - fraud_centroid, axis=1)

df_c4_nfraud['distance_to_fraud_center'] = distances

df_suspicious = df_c4_nfraud.sort_values(
    ['distance_to_fraud_center', 'probs'],
    ascending=[True, False]
)














#Step 1 — Filter Non-Frauds in Cluster 4

df_c4_nfraud = df_c4[df_c4['label'] == 0]

#Step 2 — Rank by Suspiciousness

We define suspicious non-frauds as:
	1.	High model probability (probs)
	2.	Close to fraud-dense region in embedding space
	3.	High-risk feature values (amount, length, etc.)
    
df_suspicious = df_c4_nfraud.sort_values('probs', ascending=False)
df_suspicious.head(20)

These are non-frauds with highest fraud probability inside a fraud-heavy cluster.


Step A
Cluster-Based Prior Adjustment

Since fraud rate in cluster 4 = 0.74

Create a behavioral fraud score:


cluster_fraud_rate = 0.74

df_c4_nfraud['adjusted_score'] = (
    0.5 * df_c4_nfraud['probs'] +
    0.5 * cluster_fraud_rate
)

df_suspicious = df_c4_nfraud.sort_values('adjusted_score', ascending=False)

This says:
	•	Model thinks ~0.41
	•	Cluster says ~0.74
	•	Combined score is higher

Now rank by adjusted_score.













from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30,
    n_iter=1000
)

embeddings_2d = tsne.fit_transform(embeddings_sub)










from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
emb_c4_2d = tsne.fit_transform(emb_c4)










import numpy as np

mask_c4 = (cluster_ids == 4)

emb_c4 = embeddings_sub[mask_c4]
labels_c4 = labels_sub[mask_c4]

print(emb_c4.shape)
print(labels_c4.shape)



from sklearn.cluster import KMeans

kmeans_c4 = KMeans(n_clusters=3, random_state=42)
subcluster_ids = kmeans_c4.fit_predict(emb_c4)




import pandas as pd

df_c4_new = pd.DataFrame({
    "subcluster": subcluster_ids,
    "label": labels_c4
})

df_c4_new.groupby("subcluster")["label"].agg(
    count="count",
    fraud_rate="mean"
).sort_values("fraud_rate", ascending=False)


















plt.scatter(df_c4[df_c4.label==1]['emb_2d_x'],
            df_c4[df_c4.label==1]['emb_2d_y'], alpha=0.3)

plt.scatter(df_c4[df_c4.label==0]['emb_2d_x'],
            df_c4[df_c4.label==0]['emb_2d_y'], alpha=0.3)

plt.legend(['Fraud','Non-Fraud'])
plt.show()








if logits.shape[-1] == 2:
    probs = torch.softmax(logits, dim=1)[:, 1]
else:
    probs = torch.sigmoid(logits).squeeze(-1)

all_probs.append(probs.detach().cpu().numpy())










def model_forward_with_logits(batch):

    input_ids = batch["input_ids"].to(device)
    lens = batch["lens"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):

            # Backbone
            outputs = clf_model.model(input_ids=input_ids)
            hidden_states = outputs["hidden_states"]   # 👈 IMPORTANT

            # Last valid token pooling
            idx = (lens - 1).clamp_min(0)
            pooled = hidden_states[
                torch.arange(hidden_states.size(0), device=hidden_states.device),
                idx
            ]

            # Fraud head
            pooled = clf_model.dropout(pooled)
            logits = clf_model.score(pooled)

    return hidden_states, logits







def model_forward_with_logits(batch):

    input_ids = batch["input_ids"].to(device)
    lens = batch["lens"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            
            # 1️⃣ Get backbone hidden states
            hidden_states = clf_model.model(input_ids=input_ids)
            # shape: [B, T, 2048]

            # 2️⃣ Last valid token pooling
            idx = (lens - 1).clamp_min(0)
            pooled = hidden_states[
                torch.arange(hidden_states.size(0), device=hidden_states.device),
                idx
            ]
            # shape: [B, 2048]

            # 3️⃣ Fraud head
            pooled = clf_model.dropout(pooled)
            logits = clf_model.score(pooled)
            # shape: [B, 1]

    return hidden_states, logits











def model_forward_with_logits(batch):

    input_ids = batch['input_ids'].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):

            model = clf_model.model

            x = model.token_embedding(input_ids)
            x = model.pos_embedding(x)

            for layer in model.layers:
                x = layer(x)

            hidden_states = model.norm(x)
            logits = model.lm_head(hidden_states)

    return hidden_states, logits








# Concatenate everything
embeddings = np.vstack(all_embs)          # [N, D]
labels = np.concatenate(all_labels)       # [N]
probs = np.concatenate(all_probs)         # [N]

print("Embeddings:", embeddings.shape)
print("Labels:", labels.shape)
print("Probs:", probs.shape)

# Save
np.save("/mnt/common/.../embeddings.npy", embeddings.astype(np.float32))
np.save("/mnt/common/.../labels.npy", labels.astype(np.int8))
np.save("/mnt/common/.../probs.npy", probs.astype(np.float32))

print("Saved successfully")












pooled = hidden[
    torch.arange(hidden.size(0), device=hidden.device),
    idx
]


if logits.shape[-1] == 2:
    probs = torch.softmax(logits, dim=1)[:, 1]
else:
    probs = torch.sigmoid(logits).squeeze(-1)
    
    
    
    all_probs.append(probs.detach().cpu().numpy())


print(hidden.shape)   # should be [256, T, 2048]
print(logits.shape)   # should be [256, 1] or [256, 2]
print(lens.shape)     # should be [256]
break


hidden, logits = model_forward_with_logits(batch)



def model_forward_with_logits(batch):

    input_ids = batch['input_ids'].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            outputs = clf_model.model(input_ids=input_ids)

    return outputs["hidden_states"], outputs["logits"]






def model_forward(batch):

    input_ids = batch["input_ids"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            outputs = clf_model.model(input_ids=input_ids)

    return outputs





all_embs = []
all_labels = []
all_probs = []

clf_model.model.eval()

for batch in tqdm(eval_dataloader, desc="Processing Validation Data"):

    batch = {k: v.to(device) if isinstance(v, torch.Tensor) else v
             for k, v in batch.items()}

    outputs = model_forward(batch)

    hidden_states = outputs.hidden_states[-1]   # last transformer layer
    logits = outputs.logits                     # classifier logits

    lens = batch["lens"]
    labels = batch["frd_labels"]

    # -------- Last token pooling --------
    idx = (lens - 1).clamp_min(0)
    pooled = hidden_states[torch.arange(hidden_states.size(0)), idx]

    # -------- Convert logits → probability --------
    if logits.shape[-1] == 2:
        probs = torch.softmax(logits, dim=1)[:, 1]  # probability of fraud
    else:
        probs = torch.sigmoid(logits).squeeze()

    all_embs.append(pooled.detach().cpu().numpy())
    all_labels.append(labels.detach().cpu().numpy())
    all_probs.append(probs.detach().cpu().numpy())
    
    
    
    
embeddings = np.vstack(all_embs)
labels = np.concatenate(all_labels)
probs = np.concatenate(all_probs)

print("Embeddings shape:", embeddings.shape)
print("Labels shape:", labels.shape)
print("Probs shape:", probs.shape)









base_path = "/nas/pyfrm_dev_3/mrm/pfm/debit/trans_0624_1024_byacct/"

files = [f"{base_path}part_{i}" for i in range(1, 6)]

df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)







cluster_fraud_rate = df.groupby("Cluster")["label"].mean()


fraud_rate_per_point = [cluster_fraud_rate[c] for c in cluster_ids]


plt.figure(figsize=(8,6))

plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=fraud_rate_per_point,
    cmap="Reds",
    s=5,
    alpha=0.7
)

plt.colorbar(label="Cluster Fraud Rate")
plt.title("Clusters Colored by Fraud Density")
plt.show()








import matplotlib.pyplot as plt

# Create masks
fraud_mask = labels_sub == 1
nonfraud_mask = labels_sub == 0

# Fix axis limits for fair comparison
x_min, x_max = embeddings_2d[:,0].min(), embeddings_2d[:,0].max()
y_min, y_max = embeddings_2d[:,1].min(), embeddings_2d[:,1].max()

plt.figure(figsize=(14,6))

# --- Non-Fraud ---
plt.subplot(1, 2, 1)
plt.scatter(
    embeddings_2d[nonfraud_mask, 0],
    embeddings_2d[nonfraud_mask, 1],
    s=5,
    alpha=0.6
)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.title("Non-Fraud")

# --- Fraud ---
plt.subplot(1, 2, 2)
plt.scatter(
    embeddings_2d[fraud_mask, 0],
    embeddings_2d[fraud_mask, 1],
    s=5,
    alpha=0.6
)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.title("Fraud")

plt.tight_layout()
plt.show()






import pandas as pd

df = pd.DataFrame({
    "cluster": cluster_ids,
    "label": labels_sub
})

cluster_stats = df.groupby("cluster").agg(
    count=("label", "count"),
    fraud_rate=("label", "mean")
).sort_values("fraud_rate", ascending=False)

cluster_stats









import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

plt.scatter(
    embeddings_2d[labels_sub == 0, 0],
    embeddings_2d[labels_sub == 0, 1],
    alpha=0.2,
    label="Non-Fraud"
)

plt.scatter(
    embeddings_2d[labels_sub == 1, 0],
    embeddings_2d[labels_sub == 1, 1],
    alpha=0.8,
    label="Fraud"
)

plt.legend()
plt.title("Fraud vs Non-Fraud on t-SNE Space")
plt.show()






import numpy as np

np.random.seed(42)

MAX_POINTS = 20000

fraud_idx = np.where(labels == 1)[0]
nonfraud_idx = np.where(labels == 0)[0]

# Decide how many fraud to keep (cap at MAX_POINTS // 2)
max_fraud = MAX_POINTS // 2
n_fraud = min(len(fraud_idx), max_fraud)
n_nonfraud = MAX_POINTS - n_fraud

fraud_keep = np.random.choice(
    fraud_idx,
    size=n_fraud,
    replace=False
)

nonfraud_keep = np.random.choice(
    nonfraud_idx,
    size=n_nonfraud,
    replace=False
)

selected_idx = np.concatenate([fraud_keep, nonfraud_keep])
np.random.shuffle(selected_idx)

embeddings_sub = embeddings[selected_idx]
labels_sub = labels[selected_idx]

print("Subsampled embeddings:", embeddings_sub.shape)
print("Fraud count:", labels_sub.sum())
print("Fraud ratio:", labels_sub.mean())












import numpy as np

np.random.seed(42)

MAX_POINTS = 20000  # safe size for t-SNE

fraud_idx = np.where(labels == 1)[0]
nonfraud_idx = np.where(labels == 0)[0]

# keep all fraud
fraud_keep = fraud_idx

remaining = MAX_POINTS - len(fraud_keep)

nonfraud_keep = np.random.choice(
    nonfraud_idx,
    size=remaining,
    replace=False
)

selected_idx = np.concatenate([fraud_keep, nonfraud_keep])

embeddings_sub = embeddings[selected_idx]
labels_sub = labels[selected_idx]

print("Subsampled embeddings:", embeddings_sub.shape)
print("Fraud count:", labels_sub.sum())




from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate=200,
    random_state=42
)


embeddings_2d = tsne.fit_transform(embeddings_sub)

print("t-SNE output shape:", embeddings_2d.shape)


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=6, random_state=42)
cluster_ids = kmeans.fit_predict(embeddings_2d)


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=cluster_ids,
    alpha=0.6
)
plt.title("K-Means Clusters on t-SNE Output")
plt.show()


# Fraud Concentration Per cluster


import pandas as pd

df = pd.DataFrame({
    "cluster": cluster_ids,
    "label": labels_sub
})

stats = df.groupby("cluster").agg(
    count=("label", "count"),
    fraud_rate=("label", "mean")
).sort_values("fraud_rate", ascending=False)

print(stats)



import os

out_dir = "/nas/pyfrm_dev_3/mrm/pfm/experiments/fraud_ft/clustering/tsne_runs/last_token_run_001"
os.makedirs(out_dir, exist_ok=True)



import numpy as np

np.save(f"{out_dir}/selected_idx.npy", selected_idx)
np.save(f"{out_dir}/embeddings_sub.npy", embeddings_sub)
np.save(f"{out_dir}/labels_sub.npy", labels_sub)

print("Saved sampled embeddings and labels")



embeddings_2d = tsne.fit_transform(embeddings_sub)


np.save(f"{out_dir}/embeddings_2d_tsne.npy", embeddings_2d)

print("Saved t-SNE output:", embeddings_2d.shape)


np.save(f"{out_dir}/cluster_ids.npy", cluster_ids)



# Verify Everything loads

emb2d = np.load(f"{out_dir}/embeddings_2d_tsne.npy")
labs = np.load(f"{out_dir}/labels_sub.npy")

print(emb2d.shape, labs.shape)

embeddings_2d = np.load(".../embeddings_2d_tsne.npy")
labels_sub = np.load(".../labels_sub.npy")
cluster_ids = np.load(".../cluster_ids.npy")
















import numpy as np

embeddings = np.load(f"{base_path}/embeddings.npy")
labels = np.load(f"{base_path}/labels.npy")

print("Embeddings:", embeddings.shape)
print("Labels:", labels.shape)






import numpy as np

np.random.seed(42)

# Parameters
N_NON_FRAUD = 900
N_FRAUD = 100
D = 2048

# Non-fraud: large diffuse cluster
non_fraud_embeddings = np.random.normal(
    loc=0.0,
    scale=1.0,
    size=(N_NON_FRAUD, D)
)

# Fraud: tighter cluster, slightly shifted
fraud_embeddings = np.random.normal(
    loc=1.5,
    scale=0.6,
    size=(N_FRAUD, D)
)

# Combine
embeddings = np.vstack([non_fraud_embeddings, fraud_embeddings])
labels = np.array([0] * N_NON_FRAUD + [1] * N_FRAUD)

print("Embeddings shape:", embeddings.shape)
print("Labels shape:", labels.shape)




from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate=200,
    random_state=42
)

embeddings_2d = tsne.fit_transform(embeddings)





import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

plt.scatter(
    embeddings_2d[labels == 0, 0],
    embeddings_2d[labels == 0, 1],
    alpha=0.3,
    label="Non-Fraud"
)

plt.scatter(
    embeddings_2d[labels == 1, 0],
    embeddings_2d[labels == 1, 1],
    alpha=0.8,
    label="Fraud"
)

plt.legend()
plt.title("t-SNE on Synthetic Embeddings")
plt.xlabel("t-SNE dim 1")
plt.ylabel("t-SNE dim 2")
plt.show()



from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, random_state=42)
cluster_ids = kmeans.fit_predict(embeddings)

plt.figure(figsize=(8, 6))
plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=cluster_ids,
    alpha=0.6
)
plt.title("K-Means clusters (synthetic data)")
plt.show()



hierarchy = [("A", None), ("B", "A"), ("C", "B")]

print(hierarchy)

parents = {node: parent for node, parent in hierarchy}
print("CHecking the parents:", parents)

def flatten_hierarchy(hierarchy):

    parents = {node: parent for node, parent in hierarchy}

    memo = {}

    def get_path(node):
        if node in memo:
            return memo[node]

        parent = parents[node]

        if parent is None:
            memo[node] = [node]
        else:
            memo[node] = get_path(parent) + [node]

        return memo[node]

    result = []

    for node in parents:
        result.append((node, get_path(node)))

    return result

hierarchy = [
    ("A", None),
    ("B", "A"),
    ("C", "B")
]

print(flatten_hierarchy(hierarchy))

Can you explain me this one by one