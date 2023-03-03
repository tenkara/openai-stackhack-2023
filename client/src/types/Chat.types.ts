export interface MessageI {
    id: number;
    content: string;
    sender: "bot" | "user";
}