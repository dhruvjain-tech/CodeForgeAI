"use client"

import { BellIcon, SearchIcon } from "lucide-react"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

export function AppHeader() {
  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-background px-4">
      <SidebarTrigger />
      <Separator orientation="vertical" className="h-5" />
      <InputGroup className="hidden max-w-sm sm:flex">
        <InputGroupInput placeholder="Search tasks, repos, agents..." />
        <InputGroupAddon>
          <SearchIcon aria-hidden="true" />
        </InputGroupAddon>
      </InputGroup>
      <div className="ml-auto flex items-center gap-2">
        <Button variant="ghost" size="icon" aria-label="Notifications">
          <BellIcon aria-hidden="true" />
        </Button>
        <Avatar className="size-8">
          <AvatarFallback className="bg-primary/10 text-xs font-medium text-primary">AR</AvatarFallback>
        </Avatar>
      </div>
    </header>
  )
}
