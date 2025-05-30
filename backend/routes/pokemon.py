from fastapi import APIRouter, HTTPException, Request
from db import get_connection
from langgraph_agent.pokemon_agent import generate_recommendation


router = APIRouter()

