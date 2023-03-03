import React from "react";

type Props = {
    id: number;
    sender: "bot" | "user";
    content: string;
};

export default function Message({ id, sender, content }: Props) {
    return (
        <div
            key={id}
            className="mt-4 flex items-center"
            style={{
                justifyContent: sender === "bot" ? "flex-start" : "flex-end",
            }}
        >
            <div
                className={`${
                    sender === "bot" ? "bg-primary-400" : "bg-secondary-400"
                } rounded-lg p-4 text-xl text-white max-w-[80%] break-words`}
            >
                {content}
            </div>
        </div>
    );
}
