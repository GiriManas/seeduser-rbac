Below is exactly what you need to add to your QASection.tsx.



STEP 1 — Import the new JSON


import defaultExamples from "../files/default_examples.json";


STEP 2 — Maintain a serial counter

Add a state variable to track which example is currently shown:


const [exampleIndex, setExampleIndex] = useState(0);


STEP 3 — Create a function to fetch by index (SERIAL)


const getSerialExample = (index: number) => {
  const examples = defaultExamples["RAG"]["Groundedness"]; // FIXED FOR RAG

  const safeIndex = index % examples.length;  // prevents overflow

  const item = examples[safeIndex];

  return {
    question: item["Question"],
    context: item["Context"],
    answer: item["Answer"]
  };
};



STEP 4 — Use the first example as initial state



const first = getSerialExample(0);

const [questionText, setquestionText] = useState(first.question);
const [context, setcontext] = useState(first.context);
const [answerText, setanswerText] = useState(first.answer);


STEP 5 — Update your refreshSource() to LOAD NEXT EXAMPLE

Replace your current random logic.

const refreshSource = () => {
  const nextIndex = exampleIndex + 1;

  const newExample = getSerialExample(nextIndex);

  setquestionText(newExample.question);
  setcontext(newExample.context);
  setanswerText(newExample.answer);

  setExampleIndex(nextIndex);   // move to next
};


