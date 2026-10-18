from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import add_product, find_product, get_products

app = FastAPI(title="LR4 Product API")


class ProductInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)


class ProductOutput(ProductInput):
    id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/products", response_model=ProductOutput, status_code=201)
def create_product(product: ProductInput):
    return add_product(product.name, product.price)


@app.get("/products", response_model=list[ProductOutput])
def list_products():
    return get_products()


@app.get("/products/{product_id}", response_model=ProductOutput)
def read_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
