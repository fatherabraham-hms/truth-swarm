import { cn } from "@/lib/utils";
import React, { ReactNode } from "react";

export const MaxWidthWrapper = ({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) => {
  return (
    <div className={cn("mx-auto w-full px-4", className)}>
      {children}
    </div>
  );
};