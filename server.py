#!/usr/bin/env python3
"""MCP Server for number calculations - sum and product of listed numbers."""

import json
import math
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator_mcp")


class NumberListInput(BaseModel):
    """Input model for number list operations."""

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    numbers: List[float] = Field(
        ...,
        description="List of numbers to calculate (e.g., [1, 2, 3, 4, 5])",
        min_length=1,
    )


@mcp.tool(
    name="calculate_sum",
    annotations={
        "title": "Calculate Sum",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def calculate_sum(params: NumberListInput) -> str:
    """Calculate the sum of a list of numbers.

    This tool takes a list of numbers and returns their total sum.

    Args:
        params (NumberListInput): Validated input containing:
            - numbers (List[float]): List of numbers to sum (e.g., [1, 2, 3])

    Returns:
        str: JSON string with the following schema:
            {
                "numbers": [float, ...],  # Input numbers
                "sum": float              # Sum of all numbers
            }

    Examples:
        - [1, 2, 3] -> sum = 6
        - [10, 20, 30] -> sum = 60
    """
    total = sum(params.numbers)
    return json.dumps(
        {"numbers": params.numbers, "sum": total},
        ensure_ascii=False,
    )


@mcp.tool(
    name="calculate_product",
    annotations={
        "title": "Calculate Product",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def calculate_product(params: NumberListInput) -> str:
    """Calculate the product of a list of numbers.

    This tool takes a list of numbers and returns their total product (multiplication of all).

    Args:
        params (NumberListInput): Validated input containing:
            - numbers (List[float]): List of numbers to multiply (e.g., [2, 3, 4])

    Returns:
        str: JSON string with the following schema:
            {
                "numbers": [float, ...],  # Input numbers
                "product": float          # Product of all numbers
            }

    Examples:
        - [2, 3, 4] -> product = 24
        - [1, 5, 10] -> product = 50
    """
    product = math.prod(params.numbers)
    return json.dumps(
        {"numbers": params.numbers, "product": product},
        ensure_ascii=False,
    )


@mcp.tool(
    name="calculate_sum_and_product",
    annotations={
        "title": "Calculate Sum and Product",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def calculate_sum_and_product(params: NumberListInput) -> str:
    """Calculate both sum and product of a list of numbers at once.

    This tool takes a list of numbers and returns both their sum and product.

    Args:
        params (NumberListInput): Validated input containing:
            - numbers (List[float]): List of numbers to calculate (e.g., [1, 2, 3, 4])

    Returns:
        str: JSON string with the following schema:
            {
                "numbers": [float, ...],  # Input numbers
                "sum": float,             # Sum of all numbers
                "product": float          # Product of all numbers
            }

    Examples:
        - [1, 2, 3, 4] -> sum = 10, product = 24
        - [2, 5, 10] -> sum = 17, product = 100
    """
    total = sum(params.numbers)
    product = math.prod(params.numbers)
    return json.dumps(
        {"numbers": params.numbers, "sum": total, "product": product},
        ensure_ascii=False,
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
