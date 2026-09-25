import { PageHeader } from "@/components/shared/page-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FieldGroup, Field, FieldLabel, FieldDescription } from "@/components/ui/field"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"

export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Settings" description="Configure agent behavior, approval requirements, and notifications." />

      <Card>
        <CardHeader>
          <CardTitle>Agent Autonomy</CardTitle>
          <CardDescription>Control how much agents can do without human sign-off.</CardDescription>
        </CardHeader>
        <CardContent>
          <FieldGroup>
            <Field orientation="horizontal">
              <div className="flex flex-col gap-0.5">
                <FieldLabel htmlFor="auto-merge">Auto-merge passing PRs</FieldLabel>
                <FieldDescription>Merge pull requests automatically once all checks pass.</FieldDescription>
              </div>
              <Switch id="auto-merge" />
            </Field>
            <Separator />
            <Field orientation="horizontal">
              <div className="flex flex-col gap-0.5">
                <FieldLabel htmlFor="require-review">Require human review</FieldLabel>
                <FieldDescription>Block merges on critical repositories until a human approves.</FieldDescription>
              </div>
              <Switch id="require-review" defaultChecked />
            </Field>
            <Separator />
            <Field orientation="horizontal">
              <div className="flex flex-col gap-0.5">
                <FieldLabel htmlFor="notify-failures">Notify on failed tasks</FieldLabel>
                <FieldDescription>Send a notification when an agent task fails or needs review.</FieldDescription>
              </div>
              <Switch id="notify-failures" defaultChecked />
            </Field>
          </FieldGroup>
        </CardContent>
      </Card>
    </div>
  )
}
