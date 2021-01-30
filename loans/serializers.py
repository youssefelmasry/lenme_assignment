from rest_framework import serializers
from loans.models import Loans, LoanOffers

class LoanSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['loan_amount', 'loan_period_in_month']

    def create(self, validated_data):
        validated_data['borrower'] = self.context['user']
        return super().create(validated_data)

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffers
        fields = ['loan', 'annual_interest_rate', 'accepted', 'id']
        read_only_fields = ['id']
        optional_fields = ['accepted']

    def create(self, validated_data):
        user = self.context['user']
        if user.usertype != 'investor':
            raise serializers.ValidationError({"status":"Only Investors can submit offers"})

        validated_data['investor'] = user
        validated_data.pop('accepted')
        instance = LoanOffers.objects.get_or_create(loan=self.validated_data['loan'], defaults=validated_data)[0]
        return instance

    def update(self, instance, validated_data):
        if 'accepted' not in validated_data:
            raise serializers.ValidationError({"accepted":["This field is required."]})
        user = self.context['user']
        if instance.loan.borrower != user:
            raise serializers.ValidationError({"error":"Cannot respond to this offer, Wrong user"})

        if instance.loan.loan_status != 'pending':
            raise serializers.ValidationError({"error":"This offer's loan is already funded or completed"})

        setattr(instance, 'accepted', validated_data['accepted'])
        instance.save(update_fields=['accepted'])
        return instance
   