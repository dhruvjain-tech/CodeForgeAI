import type { Project } from "@/lib/types"

export const projects: Project[] = [
  {
    id: "nexus",
    name: "Nexus",
    repository: "acme/nexus-core",
    description: "Core identity and authentication platform used across the product suite.",
    stack: ["Python", "FastAPI", "PostgreSQL", "Redis"],
    lastActivity: "12 min ago",
    codeHealth: 87,
    activeTasks: 4,
    status: "healthy",
  },
  {
    id: "procurement-assistant",
    name: "Procurement Assistant",
    repository: "acme/procurement-assistant",
    description: "AI-assisted purchase order generation and vendor matching service.",
    stack: ["TypeScript", "Next.js", "PostgreSQL"],
    lastActivity: "2 hours ago",
    codeHealth: 74,
    activeTasks: 2,
    status: "attention",
  },
  {
    id: "warehouse-management",
    name: "Warehouse Management",
    repository: "acme/wms-platform",
    description: "Inventory tracking, pick-pack-ship workflows, and warehouse telemetry.",
    stack: ["Go", "gRPC", "PostgreSQL", "Kafka"],
    lastActivity: "35 min ago",
    codeHealth: 91,
    activeTasks: 1,
    status: "healthy",
  },
  {
    id: "finance-pilot",
    name: "Finance Pilot",
    repository: "acme/finance-pilot",
    description: "Automated reconciliation and reporting for the finance operations team.",
    stack: ["Python", "Django", "MySQL"],
    lastActivity: "1 day ago",
    codeHealth: 58,
    activeTasks: 3,
    status: "critical",
  },
]

export function getProject(id: string) {
  return projects.find((p) => p.id === id)
}
