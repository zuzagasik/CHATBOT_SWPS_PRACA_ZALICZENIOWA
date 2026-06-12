import Chat from "./chat";

export default function Home() {
  return (
    <main className="min-vh-100 d-flex flex-column align-items-center justify-content-center bg-body-tertiary p-3">
      <h1 className="h3 mb-4 text-center">CHATBOT naukowy arXiv</h1>
      <Chat />
    </main>
  );
}
