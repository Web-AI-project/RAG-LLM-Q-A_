import Head from "next/head";
import FileUpload from "../components/FileUpload";
import ChatInterface from "../components/ChatInterface";

export default function Home() {
  return (
    <>
      <Head>
        <title>Document Q&A</title>
      </Head>
      <main>
        <h1>RAG-based PDF Chat</h1>
        <FileUpload />
        <ChatInterface />
      </main>
    </>
  );
}
