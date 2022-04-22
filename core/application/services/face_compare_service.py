from Interface import implements, Interface
from core.domain.services.iface_compare_service import IFaceCompareService


class FaceCompareService(implements(IFaceCompareService)):
    
    def handle(self, image_one, image_two):
        return True
    