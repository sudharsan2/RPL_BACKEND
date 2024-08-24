from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework  import generics, status, views, permissions, parsers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import (RegisterSerializer, loginSerializer)
from django.shortcuts import get_object_or_404
from .models import WorkOrderHeader
from rest_framework_simplejwt.tokens import RefreshToken
from .models import user
from .serializer import ProductionDetailSerializer





class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        userpayload = request.data

        serializer = self.serializer_class(data=userpayload)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        
        user_data = serializer.data
        user_obj = user.objects.get(email=user_data.get('email'))
        token = RefreshToken.for_user(user_obj).access_token
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class=loginSerializer
    def post(self, request):
         user = request.data
         serializer = self.serializer_class(data=user)
         serializer.is_valid(raise_exception=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    WorkOrderHeader, ProductionDetail, MaterialDetail, ScrapDetail, 
    MachineParameter, LineClearance, PolyWastageDetail, RawMaterial, 
    NcoAndOh,breakDownDetail
)
from .serializer import WorkOrderHeaderSerializer

class CreateWorkOrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            
            production_details_data = data.get('productionDetails', [])
            production_details = []
            for pd_data in production_details_data:
                pd = ProductionDetail.objects.create(
                    printedRollNo=pd_data.get('printedRollNo'),
                    printingOpName=pd_data.get('printingOpName'),
                    printedInputRollKgs=pd_data.get('printedInputRollKgs'),
                    supName=pd_data.get('supName'),
                    supRollNo=pd_data.get('supRollNo'),
                    netWt=pd_data.get('netWt'),
                    outputRollNo=pd_data.get('outputRollNo'),
                    outputRollWtKgs=pd_data.get('outputRollWtKgs'),
                    outputRollMtrs=pd_data.get('outputRollMtrs'),
                    startingTime=pd_data.get('startingTime'),
                    endTime=pd_data.get('endTime'),
                    adhGsm=pd_data.get('adhGsm')
                )
                production_details.append(pd)

            
            material_details_data = data.get('materialDetails', [])
            material_details = []
            for md_data in material_details_data:
                nco_data = md_data.get('rawMaterial', {}).get('nco', {})
                oh_data = md_data.get('rawMaterial', {}).get('oh', {})
                
                nco, created = NcoAndOh.objects.get_or_create(
                    supplier=nco_data.get('supplier'),
                    grade=nco_data.get('grade'),
                    bathNo=nco_data.get('bathNo')
                )
                oh, created = NcoAndOh.objects.get_or_create(
                    supplier=oh_data.get('supplier'),
                    grade=oh_data.get('grade'),
                    bathNo=oh_data.get('bathNo')
                )

                raw_material = RawMaterial.objects.create(
                    details=md_data.get('rawMaterial', {}).get('details'),
                    nco=nco,
                    oh=oh
                )

                material_detail = MaterialDetail.objects.create(
                    slNo=md_data.get('slNo'),
                    rawMaterial=raw_material,
                    size=md_data.get('size'),
                    mc=md_data.get('mc'),
                    input=md_data.get('input'),
                    returnMaterial=md_data.get('return'),
                    used=md_data.get('used'),
                    lineClearance=md_data.get('lineClearance'),
                    supplier=md_data.get('supplier'),
                    grade=md_data.get('grade'),
                    bathNo=md_data.get('bathNo'),
                    ratio=md_data.get('ratio'),
                    inputQty=md_data.get('inputQty')
                )
                material_details.append(material_detail)

            # Handle ScrapDetail
            scrap_data = data.get('scrapDetails', {})
            scrap_detail = ScrapDetail.objects.create(
                plainPEWastage=scrap_data.get('plainPEWastage'),
                printedWastage=scrap_data.get('printedWastage'),
                packingWaste=scrap_data.get('packingWaste'),
                laminationWaste=scrap_data.get('laminationWaste'),
                total=scrap_data.get('total')
            )

             # Handle breakDownDetail
            breakdown_data = data.get('scrapDetails', {})
            breakdown_detail = breakDownDetail.objects.create(
                sleeveChange =breakdown_data.get('sleeveChange'), 
                cleaning= breakdown_data.get('cleaning'), 
                totalProdnMin=breakdown_data.get('totalProdnMin' ),
                jobSettingMin=breakdown_data.get('jobSettingMin'),
                rollChangeMin=breakdown_data.get('rollChangeMin'),
                noPlanning=breakdown_data.get('noPlanning' ),
                breakDownMin=breakdown_data.get('breakDownMin' ),
                powerCut=breakdown_data.get('powerCut' ),
                tagRemove=breakdown_data.get('tagRemove' ),
                total=breakdown_data.get('total' ),
            )

            # Handle MachineParameter
            machine_data = data.get('machineParameters', {})
            machine_parameter = MachineParameter.objects.create(
                unwinder1=machine_data.get('unwinder1'),
                unwinder2=machine_data.get('unwinder2'),
                rewinder=machine_data.get('rewinder'),
                coatingTemp=machine_data.get('coatingTemp'),
                nipTemp=machine_data.get('nipTemp'),
                lc1 = machine_data.get('lc1'),
                ncoTemp=machine_data.get('ncoTemp'),
                ohTemp=machine_data.get('ohTemp'),
                coaterCurrent=machine_data.get('coaterCurrent'),
                nipPressure=machine_data.get('nipPressure')
            )

            # Handle LineClearance
            line_clearance_data = data.get('lineClearance', {})
            line_clearance = LineClearance.objects.create(
                solvent=line_clearance_data.get('solvent', False),
                cylinder=line_clearance_data.get('cylinder', False),
                rubberRoller=line_clearance_data.get('rubberRoller', False),
                drBlade=line_clearance_data.get('drBlade', False),
                rawMaterial=line_clearance_data.get('rawMaterial', False),
                mcSurroundings=line_clearance_data.get('mcSurroundings', False),
                wasteMatl=line_clearance_data.get('wasteMatl', False),
                printedMatl=line_clearance_data.get('printedMatl', False)
            )

            # Handle PolyWastageDetail
            poly_wastage_data = data.get('polyWastageDetails', {})
            poly_wastage_detail = PolyWastageDetail.objects.create(
                damage=poly_wastage_data.get('damage'),
                wrinkle=poly_wastage_data.get('wrinkle'),
                coreEnd=poly_wastage_data.get('coreEnd')
            )

            # Handle WorkOrderHeader
            work_order = WorkOrderHeader.objects.create(
                workOrderNo=data.get('workOrderNo'),
                customer=data.get('customer'),
                jobName=data.get('jobName'),
                sleeveSize=data.get('sleeveSize'),
                target=data.get('target'),
                produced=data.get('produced'),
                balance=data.get('balance'),
                operatorName=data.get('operatorName'),
                assistantName=data.get('assistantName'),
                date=data.get('date'),
                mcName=data.get('mcName'),
                shift=data.get('shift'),
                mcSpeed=data.get('MCspeed'),
                productionWeight=data.get('productionWeight'),
                dyanLevel=data.get('dyanLevel'),
                scrapDetails=scrap_detail,
                breakDownDetail = breakdown_detail,
                machineParameters=machine_parameter,
                lineClearance=line_clearance,
                polyWastageDetails=poly_wastage_detail
            )

            # Add ManyToMany relationships
            work_order.ProductionDetails.set(production_details)
            work_order.materialDetails.set(material_details)

            return Response({'status': 'success', 'workOrderId': work_order.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from django.http import HttpResponse
from django.template import loader

class WorkOrderDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        work_order_id = kwargs.get('id')
        
        try:
            work_order = WorkOrderHeader.objects.get(id=work_order_id)
            
            # Prepare ProductionDetails
            production_details = ProductionDetail.objects.filter(workorderheader=work_order)
            production_details_data = [{
                'printedRollNo': pd.printedRollNo,
                'printingOpName': pd.printingOpName,
                'printedInputRollKgs': pd.printedInputRollKgs,
                'supName': pd.supName,
                'supRollNo': pd.supRollNo,
                'netWt': pd.netWt,
                'outputRollNo': pd.outputRollNo,
                'outputRollWtKgs': pd.outputRollWtKgs,
                'outputRollMtrs': pd.outputRollMtrs,
                'startingTime': pd.startingTime,
                'endTime': pd.endTime,
                'adhGsm': pd.adhGsm
            } for pd in production_details]
            
            # Prepare MaterialDetails
            material_details = MaterialDetail.objects.filter(workorderheader=work_order)
            material_details_data = []
            for md in material_details:
                raw_material = md.rawMaterial
                nco = raw_material.nco
                oh = raw_material.oh
                material_details_data.append({
                    'slNo': md.slNo,
                    'rawMaterial': {
                        'details': raw_material.details,
                        'nco': {
                            'supplier': nco.supplier,
                            'grade': nco.grade,
                            'bathNo': nco.bathNo
                        },
                        'oh': {
                            'supplier': oh.supplier,
                            'grade': oh.grade,
                            'bathNo': oh.bathNo
                        }
                    },
                    'size': md.size,
                    'mc': md.mc,
                    'input': md.input,
                    'return': md.returnMaterial,
                    'used': md.used,
                    'lineClearance': md.lineClearance,
                    'supplier': md.supplier,
                    'grade': md.grade,
                    'bathNo': md.bathNo,
                    'ratio': md.ratio,
                    'inputQty': md.inputQty
                })
            
            # Prepare ScrapDetail
            scrap_detail = work_order.scrapDetails
            scrap_data = {
                'plainPEWastage': scrap_detail.plainPEWastage,
                'printedWastage': scrap_detail.printedWastage,
                'packingWaste': scrap_detail.packingWaste,
                'laminationWaste': scrap_detail.laminationWaste,
                'total': scrap_detail.total
            }

            # Prepare breakDownDetail
            breakdown_detail = work_order.breakDownDetail
            scrap_data = {
                'sleeveChange' :breakdown_detail.sleeveChange,
                'cleaning' :breakdown_detail.cleaning,
                'totalProdnMin' :breakdown_detail.totalProdnMin,
                'jobSettingMin':breakdown_detail.jobSettingMin,
                'rollChangeMin' :breakdown_detail.rollChangeMin,
                'noPlanning' :breakdown_detail.noPlanning,
                'breakDownMin' :breakdown_detail.breakDownMin,
                'powerCut' :breakdown_detail.powerCut,
                'tagRemove' :breakdown_detail.tagRemove,
                'total' :breakdown_detail.total,
            }
            
            # Prepare MachineParameter
            machine_parameter = work_order.machineParameters
            machine_data = {
                'unwinder1': machine_parameter.unwinder1,
                'unwinder2': machine_parameter.unwinder2,
                'rewinder': machine_parameter.rewinder,
                'coatingTemp': machine_parameter.coatingTemp,
                'nipTemp': machine_parameter.nipTemp,
                'lc1': machine_parameter.lc1,
                'ncoTemp': machine_parameter.ncoTemp,
                'ohTemp': machine_parameter.ohTemp,
                'coaterCurrent': machine_parameter.coaterCurrent,
                'nipPressure': machine_parameter.nipPressure
            }
            
            # Prepare LineClearance
            line_clearance = work_order.lineClearance
            line_clearance_data = {
                'solvent': line_clearance.solvent,
                'cylinder': line_clearance.cylinder,
                'rubberRoller': line_clearance.rubberRoller,
                'drBlade': line_clearance.drBlade,
                'rawMaterial': line_clearance.rawMaterial,
                'mcSurroundings': line_clearance.mcSurroundings,
                'wasteMatl': line_clearance.wasteMatl,
                'printedMatl': line_clearance.printedMatl
            }
            
            # Prepare PolyWastageDetail
            poly_wastage_detail = work_order.polyWastageDetails
            poly_wastage_data = {
                'damage': poly_wastage_detail.damage,
                'wrinkle': poly_wastage_detail.wrinkle,
                'coreEnd': poly_wastage_detail.coreEnd
            }
            
            # Prepare WorkOrderHeader response
            context = {
                'workOrderNo': work_order.workOrderNo,
                'customer': work_order.customer,
                'jobName': work_order.jobName,
                'sleeveSize': work_order.sleeveSize,
                'target': work_order.target,
                'produced': work_order.produced,
                'balance': work_order.balance,
                'operatorName': work_order.operatorName,
                'assistantName': work_order.assistantName,
                'date': work_order.date,
                'mcName': work_order.mcName,
                'shift': work_order.shift,
                'MCspeed': work_order.mcSpeed,
                'productionWeight': work_order.productionWeight,
                'dyanLevel': work_order.dyanLevel,
                'productionDetails': production_details_data,
                'materialDetails': material_details_data,
                'scrapDetails': scrap_data,
                'machineParameters': machine_data,
                'lineClearance': line_clearance_data,
                'polyWastageDetails': poly_wastage_data
            }
            
            production_count = len(context['productionDetails'])
            additional_rows = max(9 - production_count, 0)
            context['additional_rows'] = [i for i in range(additional_rows)]

            material_count = len(context['materialDetails'])
            additional_rows_material = max(4 - material_count, 0)
            context['material_Details_count'] = material_count
            context['additional_rows_material'] = [i for i in range(additional_rows_material)]

            # raw_material_count = len(context['materialDetails'])
            additional_rows_raw = max(5 - material_count, 0)
            # # context['material_Details_count'] = material_count
            context['additional_rows_raw'] = [i for i in range(additional_rows_raw)]
            context['cheating_oh'] = context['materialDetails'][0]
            print(context['cheating_oh'])

            
              
            template = loader.get_template('app/job_card.html')  
            html = template.render(context, request)
            return HttpResponse(html)
            
        except WorkOrderHeader.DoesNotExist:
            return HttpResponse('<h1>WorkOrder not found</h1>', status=404)
        except Exception as e:
            return HttpResponse(f'<h1>Error: {str(e)}</h1>', status=400)


class workOrderHeadersList(APIView):
    def get(self, request):
        instance = WorkOrderHeader.objects.all()
        serializer = WorkOrderHeaderSerializer(instance, many= True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    




import pdfkit
from django.http import HttpResponse
from django.template import loader
from rest_framework.views import APIView
from .models import WorkOrderHeader, ProductionDetail, MaterialDetail

class WorkOrderDetailPdfAPIView(APIView):
    def get(self, request, *args, **kwargs):
        work_order_id = kwargs.get('id')
        
        try:
            work_order = WorkOrderHeader.objects.get(id=work_order_id)
            
            # Prepare ProductionDetails
            production_details = ProductionDetail.objects.filter(workorderheader=work_order)
            production_details_data = [{
                'printedRollNo': pd.printedRollNo,
                'printingOpName': pd.printingOpName,
                'printedInputRollKgs': pd.printedInputRollKgs,
                'supName': pd.supName,
                'supRollNo': pd.supRollNo,
                'netWt': pd.netWt,
                'outputRollNo': pd.outputRollNo,
                'outputRollWtKgs': pd.outputRollWtKgs,
                'outputRollMtrs': pd.outputRollMtrs,
                'startingTime': pd.startingTime,
                'endTime': pd.endTime,
                'adhGsm': pd.adhGsm
            } for pd in production_details]
            
            # Prepare MaterialDetails
            material_details = MaterialDetail.objects.filter(workorderheader=work_order)
            material_details_data = []
            for md in material_details:
                raw_material = md.rawMaterial
                nco = raw_material.nco
                oh = raw_material.oh
                material_details_data.append({
                    'slNo': md.slNo,
                    'rawMaterial': {
                        'details': raw_material.details,
                        'nco': {
                            'supplier': nco.supplier,
                            'grade': nco.grade,
                            'bathNo': nco.bathNo
                        },
                        'oh': {
                            'supplier': oh.supplier,
                            'grade': oh.grade,
                            'bathNo': oh.bathNo
                        }
                    },
                    'size': md.size,
                    'mc': md.mc,
                    'input': md.input,
                    'return': md.returnMaterial,
                    'used': md.used,
                    'lineClearance': md.lineClearance,
                    'supplier': md.supplier,
                    'grade': md.grade,
                    'bathNo': md.bathNo,
                    'ratio': md.ratio,
                    'inputQty': md.inputQty
                })
            
            # Prepare ScrapDetail
            scrap_detail = work_order.scrapDetails
            scrap_data = {
                'plainPEWastage': scrap_detail.plainPEWastage,
                'printedWastage': scrap_detail.printedWastage,
                'packingWaste': scrap_detail.packingWaste,
                'laminationWaste': scrap_detail.laminationWaste,
                'total': scrap_detail.total
            }

            # Prepare breakDownDetail
            breakdown_detail = work_order.breakDownDetail
            breakdown_data = {
                'sleeveChange': breakdown_detail.sleeveChange,
                'cleaning': breakdown_detail.cleaning,
                'totalProdnMin': breakdown_detail.totalProdnMin,
                'jobSettingMin': breakdown_detail.jobSettingMin,
                'rollChangeMin': breakdown_detail.rollChangeMin,
                'noPlanning': breakdown_detail.noPlanning,
                'breakDownMin': breakdown_detail.breakDownMin,
                'powerCut': breakdown_detail.powerCut,
                'tagRemove': breakdown_detail.tagRemove,
                'total': breakdown_detail.total,
            }
            
            # Prepare MachineParameter
            machine_parameter = work_order.machineParameters
            machine_data = {
                'unwinder1': machine_parameter.unwinder1,
                'unwinder2': machine_parameter.unwinder2,
                'rewinder': machine_parameter.rewinder,
                'coatingTemp': machine_parameter.coatingTemp,
                'nipTemp': machine_parameter.nipTemp,
                'lc1': machine_parameter.lc1,
                'ncoTemp': machine_parameter.ncoTemp,
                'ohTemp': machine_parameter.ohTemp,
                'coaterCurrent': machine_parameter.coaterCurrent,
                'nipPressure': machine_parameter.nipPressure
            }
            
            # Prepare LineClearance
            line_clearance = work_order.lineClearance
            line_clearance_data = {
                'solvent': line_clearance.solvent,
                'cylinder': line_clearance.cylinder,
                'rubberRoller': line_clearance.rubberRoller,
                'drBlade': line_clearance.drBlade,
                'rawMaterial': line_clearance.rawMaterial,
                'mcSurroundings': line_clearance.mcSurroundings,
                'wasteMatl': line_clearance.wasteMatl,
                'printedMatl': line_clearance.printedMatl
            }
            
            # Prepare PolyWastageDetail
            poly_wastage_detail = work_order.polyWastageDetails
            poly_wastage_data = {
                'damage': poly_wastage_detail.damage,
                'wrinkle': poly_wastage_detail.wrinkle,
                'coreEnd': poly_wastage_detail.coreEnd
            }
            
            # Prepare WorkOrderHeader response
            context = {
                'workOrderNo': work_order.workOrderNo,
                'customer': work_order.customer,
                'jobName': work_order.jobName,
                'sleeveSize': work_order.sleeveSize,
                'target': work_order.target,
                'produced': work_order.produced,
                'balance': work_order.balance,
                'operatorName': work_order.operatorName,
                'assistantName': work_order.assistantName,
                'date': work_order.date,
                'mcName': work_order.mcName,
                'shift': work_order.shift,
                'MCspeed': work_order.mcSpeed,
                'productionWeight': work_order.productionWeight,
                'dyanLevel': work_order.dyanLevel,
                'productionDetails': production_details_data,
                'materialDetails': material_details_data,
                'scrapDetails': scrap_data,
                'machineParameters': machine_data,
                'lineClearance': line_clearance_data,
                'polyWastageDetails': poly_wastage_data
            }
            
            # Prepare additional row logic for rendering in template
            production_count = len(context['productionDetails'])
            additional_rows = max(9 - production_count, 0)
            context['additional_rows'] = [i for i in range(additional_rows)]

            material_count = len(context['materialDetails'])
            additional_rows_material = max(4 - material_count, 0)
            context['material_Details_count'] = material_count
            context['additional_rows_material'] = [i for i in range(additional_rows_material)]

            additional_rows_raw = max(5 - material_count, 0)
            context['additional_rows_raw'] = [i for i in range(additional_rows_raw)]
            context['cheating_oh'] = context['materialDetails'][0]

            # Render the template to HTML
            template = loader.get_template('app/job_card.html')  
            html_content = template.render(context, request)
            
            # Convert HTML to PDF using pdfkit
            # Set path for wkhtmltopdf
            # path_to_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  
            # config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

            # Generate the PDF
            # pdf = pdfkit.from_string(html_content, False, configuration=config)
            pdf = pdfkit.from_string(html_content, False)  # False makes it return PDF as a binary instead of saving it
            
            # Send PDF as response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="work_order_{work_order_id}.pdf"'
            return response
        
        except WorkOrderHeader.DoesNotExist:
            return HttpResponse('<h1>WorkOrder not found</h1>', status=404)
        except Exception as e:
            return HttpResponse(f'<h1>Error: {str(e)}</h1>', status=400)
