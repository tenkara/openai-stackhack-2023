import React from "react";
import { Header as MHeader } from "@mantine/core";
import Image from "next/image";

type Props = {};

export default function Header({}: Props) {
    return (
        <MHeader height={70}>
            <div className="h-full bg-primary-50">
                <div className="mx-auto flex h-full max-w-5xl items-center ">
                    <Image
                        src="/logo.svg"
                        alt="Smarthealth logo"
                        width={200}
                        height={50}
                    />
                </div>
            </div>
        </MHeader>
    );
}
