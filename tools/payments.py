"""
Payment Processing Tool
Handle Stripe payments and billing.
"""

import logging
from typing import Dict, Any, Optional

from config import config

logger = logging.getLogger(__name__)


class PaymentTool:
    """Payment processing."""
    
    def __init__(self):
        """Initialize payment tool."""
        import stripe
        stripe.api_key = config.payment.stripe_key
        self.stripe = stripe
    
    async def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        description: str = "",
    ) -> Dict[str, Any]:
        """
        Create Stripe payment intent.
        
        Args:
            amount: Amount in cents
            currency: Currency code
            description: Payment description
            
        Returns:
            dict: {success, result, error}
        """
        try:
            intent = self.stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                description=description,
            )
            
            logger.info(f"Payment intent created: {intent.id}")
            return {
                "success": True,
                "result": {
                    "intent_id": intent.id,
                    "client_secret": intent.client_secret,
                    "amount": amount,
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create payment intent failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_payment_status(self, intent_id: str) -> Dict[str, Any]:
        """
        Get payment intent status.
        
        Args:
            intent_id: Payment intent ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            intent = self.stripe.PaymentIntent.retrieve(intent_id)
            
            return {
                "success": True,
                "result": {
                    "status": intent.status,
                    "amount": intent.amount,
                    "currency": intent.currency,
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get payment status failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def create_invoice(
        self,
        customer_email: str,
        amount: int,
        description: str = "",
    ) -> Dict[str, Any]:
        """
        Create invoice.
        
        Args:
            customer_email: Customer email
            amount: Invoice amount in cents
            description: Invoice description
            
        Returns:
            dict: {success, result, error}
        """
        try:
            # Find or create customer
            customers = self.stripe.Customer.list(email=customer_email)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = self.stripe.Customer.create(email=customer_email)
            
            # Create invoice items
            self.stripe.InvoiceItem.create(
                customer=customer.id,
                amount=amount,
                currency="usd",
                description=description,
            )
            
            # Create invoice
            invoice = self.stripe.Invoice.create(customer=customer.id)
            invoice.send_invoice()
            
            logger.info(f"Invoice created: {invoice.id}")
            return {
                "success": True,
                "result": {
                    "invoice_id": invoice.id,
                    "customer_id": customer.id,
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create invoice failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def list_transactions(self, limit: int = 10) -> Dict[str, Any]:
        """
        List recent transactions.
        
        Args:
            limit: Max results
            
        Returns:
            dict: {success, result, error}
        """
        try:
            charges = self.stripe.Charge.list(limit=limit)
            
            results = []
            for charge in charges.data:
                results.append({
                    "id": charge.id,
                    "amount": charge.amount,
                    "currency": charge.currency,
                    "status": charge.status,
                    "created": charge.created,
                })
            
            return {
                "success": True,
                "result": results,
                "error": None,
            }
        except Exception as e:
            logger.error(f"List transactions failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
payment_tool = PaymentTool()
