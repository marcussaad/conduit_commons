from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from conduit_commons.enums.gender_enum import GenderEnum


class ICDPayload(BaseModel):
    icd_code: str
    icd_description: str = None


class CheckoutPropertyPayload(BaseModel):
    key: str
    value: Optional[str] = None
    validation_type: Optional[str] = None


class ProductPayload(BaseModel):
    product_id: str = None
    quantity: int = None
    hcpc_code: str = None
    refill_amount: int = 1
    icds: List[ICDPayload] = []
    title: str = None
    description: str = None
    categories: Optional[List[str]] = []
    checkout_properties: Optional[List[CheckoutPropertyPayload]] = []

    class Config:
        orm_mode = True


class AddressPayload(BaseModel):
    street: str = None
    city: str = None
    state: str = None
    zip_code: str = None
    complement: Optional[str] = None

    class Config:
        orm_mode = True


class SupplierPayload(BaseModel):
    supplier_id: int = None
    supplier_name: str = None
    organization_id: str = None
    npi: str = None
    phone: str = None
    products: List[ProductPayload]
    address: Optional[AddressPayload] = None

    class Config:
        orm_mode = True


class PhysicianPayload(BaseModel):
    id: int = None
    first_name: str = None
    last_name: str = None
    npi: str = None
    phone: str = None
    email: str = None
    patient_last_visit: date = None
    address: AddressPayload = None

    class Config:
        orm_mode = True


class CaregiverPayload(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class PatientPayload(BaseModel):
    id: Optional[int] = None
    first_name: str = None
    last_name: str = None
    dob: date = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: GenderEnum = None

    class Config:
        orm_mode = True


class InsuranceEligibilityStatusPayload(BaseModel):
    status: str
    reason: Optional[str] = None


class InsurancePayload(BaseModel):
    id: Optional[int] = None
    member_id: Optional[str] = None
    group_number: str
    plan_code: str
    name: str
    state: str
    eligibility_status: Optional[InsuranceEligibilityStatusPayload] = None

    class Config:
        orm_mode = True


class OrderPayload(BaseModel):
    order_id: int
    user_id: str
    organization_id: Optional[int] = None
    patient_id: int = None
    order_date: datetime
    patient: PatientPayload = None
    caregiver: Optional[CaregiverPayload] = None
    insurance: InsurancePayload
    secondary_insurance: Optional[InsurancePayload] = None
    shipping_address: AddressPayload
    suppliers: List[SupplierPayload]
    physician: PhysicianPayload = None
    additional_information: Optional[str] = None


class UpdateInsurancePayload(BaseModel):
    order_id: int
    patient_id: int
    insurance: InsurancePayload


class UpdateProductsPayload(BaseModel):
    order_id: int
    supplier: SupplierPayload
    insurance: InsurancePayload


class UploadPayload(BaseModel):
    order_id: int
    filename: str
    user_id: str


class UploadOrderDocumentsPayload:
    data: UploadPayload
    status: str
    message: str

    def __init__(self, *args, **kwargs):
        self.data = UploadPayload(**kwargs.get("data"))
        self.status = kwargs.get("status", "")
        self.message = kwargs.get("message", "")


class DeleteFilePayload(BaseModel):
    order_id: int
    user_id: str
    key: str


class ValidateDeleteFilePayload:
    data: DeleteFilePayload
    status: str
    message: str

    def __init__(self, *args, **kwargs):
        self.data = DeleteFilePayload(**kwargs.get("data"))
        self.status = kwargs.get("status", "")
        self.message = kwargs.get("message", "")


class InsuranceEligibilityPayload(BaseModel):
    order_id: int
    user_id: str
    organization_id: int
    patient_id: int
    insurance: InsurancePayload


class OrderInsuranceEligibilityPayload:
    data: InsuranceEligibilityPayload
    status: str
    message: str

    def __init__(self, *args, **kwargs):
        self.data = InsuranceEligibilityPayload(**kwargs.get("data"))
        self.status = kwargs.get("status", "")
        self.message = kwargs.get("message", "")
