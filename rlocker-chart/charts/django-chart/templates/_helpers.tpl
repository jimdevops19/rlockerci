{{- define "django-chart.secret" -}}
{{- default .Values.global.django.secret -}}
{{- end }}

{{- define "django-chart.debug" -}}
{{- default .Values.global.django.debug -}}
{{- end }}

{{- define "django-chart.postgresqlUser" -}}
{{- default .Values.global.django.postgresqlUser -}}
{{- end }}

{{- define "django-chart.postgresqlPassword" -}}
{{- default .Values.global.django.postgresqlPassword -}}
{{- end }}

{{- define "django-chart.postgresqlDatabase" -}}
{{- default .Values.global.django.postgresqlDatabase -}}
{{- end }}

{{- define "django-chart.superuserUsername" -}}
{{- default .Values.global.django.superuserUsername -}}
{{- end }}

{{- define "django-chart.superuserPassword" -}}
{{- default .Values.global.django.superuserPassword -}}
{{- end }}

{{- define "django-chart.superuserEmail" -}}
{{- default .Values.global.django.superuserEmail -}}
{{- end }}

{{ define "django-chart.Image" }}
    {{- printf "%s:%s" .Values.global.images.django.url .Values.global.images.django.tag -}}
{{- end }}