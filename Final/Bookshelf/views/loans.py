from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Loan
from ..forms import LoanForm

@login_required
def loans_view(request):
    loans = Loan.objects.all()

    if request.method == 'POST':
        if 'return_loan' in request.POST:
            loan_id = request.POST.get('return_loan')
            Loan.objects.filter(id=loan_id).delete()
            return redirect('loans')
        else:
            form = LoanForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('loans')
    else:
        form = LoanForm()

    return render(request, 'books/loans.html', {
        'form': form,
        'loans': loans,
    })

