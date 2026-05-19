from __future__ import annotations

import secrets
from dataclasses import dataclass


P = 2**255 - 19
G = 5


@dataclass(slots=True)
class SchnorrProof:
    commitment: int
    challenge: int
    response: int


class SchnorrZKP:
    def __init__(self, secret: int | None = None) -> None:
        self.secret = secret or secrets.randbelow(P - 2) + 1
        self.public = pow(G, self.secret, P)

    def prove(self) -> SchnorrProof:
        nonce = secrets.randbelow(P - 2) + 1
        commitment = pow(G, nonce, P)
        challenge = secrets.randbelow(P - 2) + 1
        response = (nonce + challenge * self.secret) % (P - 1)
        return SchnorrProof(commitment=commitment, challenge=challenge, response=response)

    @staticmethod
    def verify(public: int, proof: SchnorrProof) -> bool:
        left = pow(G, proof.response, P)
        right = (proof.commitment * pow(public, proof.challenge, P)) % P
        return left == right
