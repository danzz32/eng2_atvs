package delivery.demo.entityTests;

import delivery.demo.model.Cidade;
import delivery.demo.repository.CidadeRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

@ActiveProfiles("test")
@DataJpaTest
public class CidadeRepositoryTest {

    @Autowired
    private CidadeRepository cidadeRepository;

    @Test
    @DisplayName("Deve salvar e buscar a cidade por UF")
    void deveSalvarEBuscarCidadePorUf() {
        cidadeRepository.save(new Cidade("São Luís", "MA", 15.0));
        cidadeRepository.save(new Cidade("Imperatriz", "MA", 8.5));
        cidadeRepository.save(new Cidade("Açailândia", "MA", 9.6));

        List<Cidade> resultado = cidadeRepository.findByUf("MA");
        assertThat(resultado).hasSize(3);
    }
}
