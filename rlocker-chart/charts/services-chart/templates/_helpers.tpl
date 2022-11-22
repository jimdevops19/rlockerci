{{- define "services-chart.resourceLockerToken" -}}
{{- default .Values.global.queue_service.resourceLockerToken -}}
{{- end }}

{{- define "services-chart.resourceLockerUrl" -}}
{{- default .Values.global.queue_service.resourceLockerUrl -}}
{{- end }}

{{- define "services-chart.tag" -}}
{{- default .Values.global.queue_service.tag -}}
{{- end }}

{{ define "services-chart.queueServiceImage" }}
    {{- printf "%s:%s" .Values.global.images.queue_service.url .Values.global.images.queue_service.tag -}}
{{- end }}