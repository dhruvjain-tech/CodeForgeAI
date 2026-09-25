import Link from "next/link"
import { ArrowRightIcon, LightbulbIcon } from "lucide-react"

import { advisorAnalysis, currentStack } from "@/lib/data/tech-advisor"

import { PageHeader } from "@/components/shared/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function TechAdvisorPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Tech Advisor"
        description="Continuous evaluation of the current stack against viable alternatives, grounded in production telemetry."
      />

      <Card>
        <CardHeader>
          <CardTitle>Current Stack</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {currentStack.map((tech) => (
            <div key={tech.name} className="flex flex-col gap-0.5 rounded-lg border border-border px-3 py-2">
              <span className="text-sm font-medium text-foreground">{tech.name}</span>
              <span className="text-xs text-muted-foreground">{tech.role}</span>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-3">
          <div className="flex flex-col gap-1">
            <CardTitle className="flex items-center gap-2">
              <span>{advisorAnalysis.target}</span>
              <ArrowRightIcon className="size-4 text-muted-foreground" aria-hidden="true" />
              <Badge variant="secondary">{advisorAnalysis.alternative}</Badge>
            </CardTitle>
          </div>
          <Button  variant="outline" size="sm">
            <Link href="/benchmarks">
              View Benchmarks
              <ArrowRightIcon aria-hidden="true" />
            </Link>
          </Button>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Alert>
            <LightbulbIcon aria-hidden="true" />
            <AlertTitle>Verdict</AlertTitle>
            <AlertDescription>{advisorAnalysis.verdict}</AlertDescription>
          </Alert>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {advisorAnalysis.sections.map((section) => (
              <div key={section.label} className="flex flex-col gap-1 rounded-lg border border-border p-4">
                <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  {section.label}
                </span>
                <p className="text-sm text-foreground">{section.summary}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
