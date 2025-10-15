import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { AgentScoring } from "@/lib/queries/agents-scoring-queries"
import React from "react";

interface AgentCardProps {
    scoring: AgentScoring;
}

export function AgentCard(scoring: AgentCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Agent</CardTitle>
                <CardDescription>Agent Name</CardDescription>
                <CardAction>Refresh</CardAction>
            </CardHeader>
            <CardContent>
                <p>{scoring.scoring.mockValue1} </p>
                <p>{scoring.scoring.mockValue2} </p>
                <p>{scoring.scoring.mockValue3} </p>
            </CardContent>
            <CardFooter className="flex text-center justify-center">
                <p>human in the loop verification with signatures?</p>
            </CardFooter>
        </Card>
    )
}