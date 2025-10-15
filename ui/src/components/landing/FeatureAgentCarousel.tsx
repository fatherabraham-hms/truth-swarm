"use client";

import { useState, useEffect, use } from "react";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import { type CarouselApi } from "@/components/ui/carousel"
import { AgentCard } from "../agents/AgentCard";
import { useAgents } from "@/hooks/useAgents";
import { RefreshCw } from "lucide-react";
import { AgentScoring } from "@/lib/queries/agents-scoring-queries";


export function FeatureAgentsCarousel() {
  const [api, setApi] = useState<CarouselApi>()
  const [current, setCurrent] = useState(0)
  const [count, setCount] = useState(0)

  useEffect(() => {
    if (!api) {
      return
    }
 
    setCount(api.scrollSnapList().length)
    setCurrent(api.selectedScrollSnap() + 1)
 
    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1)
    })
  }, [api])
 

  const { getMockAgentsScoring } = useAgents();

  if (getMockAgentsScoring.error) {
    return (
      <>
        <div>Error getting Agents Data</div>
        <div>{getMockAgentsScoring.error.message}</div>
      </>
    )
  }

  if (getMockAgentsScoring.isLoading) {
    return (
      <>
        <br />
        <RefreshCw className="w-5 h-5 animate-spin text-muted-foreground mr-2" />
        <span className="text-sm text-muted-foreground">
          Loading agents scoring...
        </span>
      </>
    )
  }

  const mockScorings: AgentScoring[] | undefined = getMockAgentsScoring.data;

  if (!mockScorings) {
    return (
      <>
        <div>No scorings found</div>
      </>
    )

  }

  const mockScoring1 = mockScorings[0];
  const mockScoring2 = mockScorings[1];
 

  return (
    <Carousel setApi={setApi}>
      <CarouselContent>
        <CarouselItem> 
          <AgentCard scoring={mockScoring1}/> 
        </CarouselItem>
        <CarouselItem>
          <AgentCard scoring={mockScoring2}/> 
        </CarouselItem>
        <CarouselItem>...</CarouselItem>
      </CarouselContent>
    </Carousel>
  )
}