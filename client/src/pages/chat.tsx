import Message from "@/components/chat/Message";
import Header from "@/components/shell/Header";
import useChat from "@/hooks/useChat";
import { MessageI } from "@/types/Chat.types";
import axios from "axios";
import React, { FormEvent } from "react";
import { BsChevronRight } from "react-icons/bs";
import { FiSend } from "react-icons/fi";
import PendingMessage from "./../components/chat/PendingMessage";

type Props = {};

export default function Chat({}: Props) {
    const [input, setInput] = React.useState("");
    const [messages, setMessages] = React.useState<MessageI[]>([]);
    const [loading, setLoading] = React.useState(false);

    const handleSendMessage = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (input === "") return;

        const newMessage = {
            id: messages.length + 1,
            content: input,
            role: "user",
        };

        setMessages([...messages, newMessage] as MessageI[]);

        try {
            setLoading(true);
            const { data } = await axios.post("/api/chat", {
                messages: [
                    ...messages.map(({ content, role }) => ({ content, role })),
                    { content: input, role: "user" },
                ],
            });
            console.log(data);

            setMessages([...messages, newMessage, data] as MessageI[]);
        } catch {}
        setLoading(false);
        setInput("");
    };

    return (
        <div className="flex min-h-screen flex-col bg-primary-50">
            <Header />
            <div className="mx-auto flex w-full max-w-4xl grow flex-col">
                <div className="flex grow flex-col  justify-end p-4">
                    {messages.map(({ role, content }, i) => (
                        <Message
                            key={"message-" + i}
                            role={role}
                            content={content}
                        />
                    ))}
                    {loading && <PendingMessage />}
                </div>

                <form
                    onSubmit={handleSendMessage}
                    className="sticky bottom-0 mb-10 flex items-stretch bg-primary-50 p-4 text-xl text-text"
                >
                    <div className=" flex items-center rounded-l bg-white px-2">
                        <BsChevronRight />
                    </div>
                    <input
                        className="z-[10] h-14 grow bg-white py-2 px-2"
                        placeholder="Type your message here..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                    />
                    <button
                        className="flex cursor-pointer items-center rounded-r bg-white px-4 hover:bg-gray-200"
                        type="submit"
                    >
                        <FiSend />
                    </button>
                </form>
            </div>
        </div>
    );
}
