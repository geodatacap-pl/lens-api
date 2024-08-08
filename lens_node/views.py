from .models import Endpoint, Detection
from .serializers import DetectionSerializer, EndpointSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date


class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = (AllowAny,)


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    permission_classes = (AllowAny,)

    def post(self, request, pk=None):
        token_debug = 'sd1234endpoint1234test'
        # print(request)
        if request.data['token'] == token_debug:
            device_id = request.data['device_id']
            endpoint_id = request.data['endpoint_id']
            resolution = request.data['resolution']
            content = request.data['content']
            datestamp = request.data['datestamp']

            for key in content:
                Detection.objects.create(
                    endpoint=Endpoint.objects.get(id=int(endpoint_id)),
                    device_id=device_id,
                    resolution=resolution,
                    detectionclass=key,
                    timestamp=datestamp,
                    accuracy=content[key]['accuracy'],
                    position_x=content[key]['pos_x'],
                    position_y=content[key]['pos_y'],
                    width=content[key]['width'],
                    height=content[key]['height'],
                    count=content[key]['count']
                )

            return Response('created')
        else:
            return Response('error')


class DetectionNewest(viewsets.ModelViewSet):
    queryset = Detection.objects.all().order_by('timestamp')[:2000]
    serializer_class = DetectionSerializer
    permission_classes = (AllowAny,)


class DetectionByDeviceNewest(viewsets.ReadOnlyModelViewSet):
    queryset = Detection.objects.all().order_by('timestamp')
    serializer_class = DetectionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        device_id = self.request.query_params.get('device_id', None)

        if device_id is not None:
            # Find the latest timestamp for the specified device_id
            latest_timestamp = Detection.objects.filter(device_id=device_id).order_by('-timestamp').first().timestamp
            # Calculate the timestamp for two days after the latest timestamp
            two_days_before = latest_timestamp - timedelta(days=2)
            queryset = Detection.objects.filter(device_id=device_id, timestamp__gte=two_days_before).order_by(
                'timestamp')
        else:
            queryset = Detection.objects.all().order_by('timestamp')

        return queryset


class DetectionByDevice(viewsets.ReadOnlyModelViewSet):
    queryset = Detection.objects.all().order_by('timestamp')
    serializer_class = DetectionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Detection.objects.all().order_by('timestamp')
        device_id = self.request.query_params.get('device_id', None)

        start_date_param = self.request.query_params.get('start_date', None)
        end_date_param = self.request.query_params.get('end_date', None)

        date_format = '%Y-%m-%dT%H:%M'
        date_start = datetime.strptime(start_date_param, date_format)
        date_end = datetime.strptime(end_date_param, date_format)

        if date_start is not None and date_end is not None:
            queryset = queryset.filter(timestamp__range=[date_start, date_end])

        if device_id is not None:
            queryset = queryset.filter(device_id=device_id)
        return queryset


class DeviceList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Detection.objects.values('device_id').distinct()
        return Response(queryset)
