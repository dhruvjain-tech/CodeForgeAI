"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  BrainIcon,
  ClipboardListIcon,
  FlaskConicalIcon,
  FolderKanbanIcon,
  GaugeIcon,
  GitBranchIcon,
  LayoutDashboardIcon,
  LineChartIcon,
  SettingsIcon,
  ShieldCheckIcon,
  SparklesIcon,
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const navigation = [
  {
    label: "Workspace",
    items: [
      { title: "Dashboard", url: "/", icon: LayoutDashboardIcon },
      { title: "Projects", url: "/projects", icon: FolderKanbanIcon },
      { title: "Tasks", url: "/tasks", icon: ClipboardListIcon },
    ],
  },
  {
    label: "Engineering",
    items: [
      { title: "Agents", url: "/agents", icon: SparklesIcon },
      { title: "Code Health", url: "/code-health", icon: ShieldCheckIcon },
      { title: "Technology Advisor", url: "/tech-advisor", icon: GaugeIcon },
      { title: "Benchmarks", url: "/benchmarks", icon: FlaskConicalIcon },
    ],
  },
  {
    label: "Intelligence",
    items: [
      { title: "Memory", url: "/memory", icon: BrainIcon },
      { title: "Evaluations", url: "/evaluations", icon: LineChartIcon },
    ],
  },
  {
    label: "Integrations",
    items: [{ title: "GitHub", url: "/github", icon: GitBranchIcon }],
  },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-sidebar-border">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              render={<Link href="/" />}
            >
              <div className="flex size-8 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground">
                <SparklesIcon className="size-4" aria-hidden="true" />
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold">CodeForge</span>
                <span className="text-xs text-muted-foreground">Agent Platform</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        {navigation.map((group) => (
          <SidebarGroup key={group.label}>
            <SidebarGroupLabel>{group.label}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => {
                  const isActive = pathname === item.url
                  return (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton
  isActive={isActive}
  tooltip={item.title}
  render={<Link href={item.url} />}
>
  <item.icon aria-hidden="true" />
  <span>{item.title}</span>
</SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarFooter className="border-t border-sidebar-border">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
  tooltip="Settings"
  isActive={pathname === "/settings"}
  render={<Link href="/settings" />}
>
  <SettingsIcon aria-hidden="true" />
  <span>Settings</span>
</SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
